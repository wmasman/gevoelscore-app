# Timeline triage methodology

**Status**: working document, locked 2026-06-10. Updated as the user's
triage practice matures.

This document captures the calibration rules and conventions used when
triaging calendar events and day-entry notes into
[`data/annotations.yaml`](data/annotations.yaml). The goal is
**consistency across all triage rounds** (calendar years 2022 to 2026,
notes topical CSVs, and any future batches) so that load values and
event-labels mean the same thing wherever they appear.

For data sources, file layout, and data-quality caveats, see
[`README.md`](README.md).

## 0. Strategic frame: per-day context database for research

The work in this folder is **not** building a visual product. It is
building a **per-day contextual database** that supports two distinct
downstream uses:

| use | inputs | how the database is consumed |
|---|---|---|
| **Quantitative / statistical** | Daily gevoelscore + per-day intensity vectors (cognitief / fysiek / emotioneel 1-3, codified through triage of day-entry notes + calendar events) | Numerical correlation with Garmin biometric channels; trajectory analysis; trigger-window hypothesis tests |
| **Qualitative / backward sensemaking** | Calendar events, episodes (umbrellas), notes-derived key events, medical records | Story-level interpretation of what was happening around any specific date or pattern |

The per-day intensity vectors are not a separate data collection. They are
**the codified form of what was already written in the notes and calendar
events**: each year's bulk triage round walks through the existing notes
and calendar context and assigns 1-3 values where the day's content supports
it. A day with rich notes about a wedding gets loads; a day with no notes
and no events stays blank. This means the vectors inherit the same coverage
gaps as the source material (see §3a on symptom-mention asymmetry).

The rendered timeline (`output/timeline.png`) is a **verification tool**
for catching gaps and duplicates during triage. It is not the product;
it is a quality-control view onto the database.

### Sources composing the per-day database

| source | content | format | maturity |
|---|---|---|---|
| Directus `day_entries.score` | daily gevoelscore (1-10) | research export | locked |
| Directus `day_entries.note` | daily free-text reflection | research export | locked (frozen at 686 days with text) |
| Directus `calendar_events` | calendar entries (work + private) | live + research export | live; coverage starts 2022-06-17 |
| `labels_crash_v2.csv` | research-derived crash + dip labels | research artefact | locked |
| `annotations.yaml` | curated events, episodes, umbrellas, interventions | this folder | active; updates each triage round |
| medical records (future) | doctor / specialist / treatment records | not yet integrated | planned |
| per-day intensity vectors | manual cognitief / fysiek / emotioneel 1-3 (cog/phy/emo), codified per year from notes + calendar | [`data/per_day_intensity.csv`](data/per_day_intensity.csv) | active; 2022-2026 done (2026-06-11) |
| PwC reintegration daily hours (2022-2024) | objective daily work-hours log + illness/visit notes during reintegration | [`data/reintegration_hours_2022-2024.csv`](data/reintegration_hours_2022-2024.csv) | added 2026-06-11 from original "Reintegratie Willem.xlsx"; 239 days covered |

### Per-day record (computed view, not a stored file)

A "per-day record" can always be computed on demand by intersecting
these sources for a given date. Conceptually:

```
date
  gevoelscore                     # day_entries.score
  crash_or_dip_label              # labels_crash_v2.csv (if applicable)
  events_today                    # annotations.yaml spans + markers where date matches
  umbrellas_today                 # annotations.yaml long levensgebeurtenis spans containing date
  free_text_note                  # day_entries.note
  per_day_intensity (future)      # planned mentaal / fysiek / cognitief vector
```

The `enrich_notes_with_existing.py` script is one realisation of this
view, materialised into the `existing_on_day` column of the notes
triage CSVs. Future analyses may build their own per-day projections.

## 1. The triage question

For every candidate row (a calendar event or a notes-extracted day),
the user is answering one question:

> **Does this row represent a discrete event worth placing on the
> per-day contextual database as standalone context for that date
> (and the dates around it)?**

Marking a row `keep_yn = y` adds an entry to `annotations.yaml`,
which then enters the per-day record whenever the date is consumed.
Marking `n` (or leaving it blank) keeps the row in the source CSV as
descriptive context — still retrievable for ad-hoc lookup, future
re-triage, or notes-text searches — but it does not get a structured
entry.

**The triage decision is about structuring, not about importance.**
A note saying "felt tired" on a generic day might be deeply relevant
to the qualitative narrative but it does not need a separate
structured event — the note text itself is already in the per-day
record via `day_entries.note`.

## 2. The 1-3 load scale (locked across all triage sources)

The `cognitive_load`, `physical_load`, and `emotional_load` columns
use a single shared scale in every triage CSV (calendar and notes):

| value | meaning |
|:-:|---|
| 1 | mild intensity on that axis (low draw on cognitive / physical / emotional reserves) |
| 2 | moderate intensity (notable draw, but recoverable within the day) |
| 3 | severe intensity (heavy draw on reserves) |
| blank | not applicable / not assessed for this axis |

**Important**: the load values capture the **intensity of the event
itself**, not the size of any after-effect (overload, crash, fatigue).
A wedding that left the user exhausted for three days has the same
load values as a wedding that did not, if the event itself was
equally intense. The after-effect lives in the timeline as a separate
phenomenon (research-derived crash labels, or notes-derived overload
events with their own labels).

This rule was set on 2026-06-10 after a brief inconsistency was
flagged: an earlier suggestion proposed using 1-3 for "overload
severity" in the notes-overload CSV, which would have produced load
values that meant something different than in the calendar CSVs.
The locked rule is: **the load scale is always about event
intensity, never about after-effect severity**.

### 2a. Per-event loads vs per-day loads (locked 2026-06-10)

A single day can host multiple load-bearing events (a tandarts visit
in the morning + a wedding in the evening). Each event carries its
own per-event load profile (the cog/phy/emo columns in the triage
CSVs). These per-event loads describe the **intensity of that
specific event**.

For statistical analysis (correlating with gevoelscore + Garmin
biometrics), the database needs **per-day** load values: one cog,
one phy, one emo value per date. A day with multiple loaded events
must therefore be consolidated.

**Consolidation model**:

| situation | how the per-day value is obtained |
|---|---|
| Day with one load-bearing event | use that event's loads directly (but see §2b — multi-day events do not contribute) |
| Day with multiple load-bearing events | **manual consolidation by the user** — the user reviews the event cluster and assigns a unified per-day value in `data/per_day_intensity.csv` |
| Day with no load-bearing event but with notes | per-day intensity triage round (planned) — user assigns loads based on the day's note and events |
| Day with no notes and no events | no per-day intensity assignment; statistical analyses must treat as missing |

The per-event loads are **preserved** even after consolidation. They
remain on the per-event entry in the source triage CSVs as
descriptive metadata. The unified per-day score lives in
[`data/per_day_intensity.csv`](data/per_day_intensity.csv) — that
file is the **source of truth for per-day intensity values**.

Rationale: MAX-aggregation across per-event loads was considered and
rejected. Two events both rated cog=2 on the same day may be
experienced as cog=3 cumulatively, or remain cog=2 if recoverable
between them. Only the user can decide.

### 2b. No generic loads on multi-day spans (locked 2026-06-10)

A multi-day span (any event where `end > start`) does **not** get its
load values propagated into `annotations.yaml`'s note field. Both
mergers strip the `load:` prefix when the span is multi-day.

Rationale (user's principle, 2026-06-10): "loads should only be on
specific days when something specific happened — either from a
calendar event for that day, from interpretation of the notes for
that day, or from another specific event on that day. A generic
load applied across a multi-day trajectory inflates every day in
the span." Examples:

- A 7-day ski trip rated `c3/p2/e2` would, under MAX-aggregation,
  make every one of those 7 days look like c3/p2/e2 in the per-day
  database. But the actual experience varies: travel day, skiing
  day, restaurant day, rest day. Per-day intensity must come from
  per-day specifics, not a blanket trajectory rating.

The raw per-event loads still live in the source triage CSVs as
historical / descriptive data. They are recoverable; they just do
not drive the per-day intensity layer.

### 2c. Triage notes as a second-order source

When the user does per-day intensity triage (cog/phy/emo per date in
`per_day_intensity_YYYY.csv`), they often write **triage notes** that
contain valuable secondary information beyond the load values:

- Event names that did not appear in the calendar export
- Symptom or context observations
- Explicit "this is a dip day despite the 4" annotations
- Pointers to missing v2 categorisation tags

These triage notes are processed by
[`scripts/classify_triage_notes.py`](scripts/classify_triage_notes.py)
(heuristic bucketing) and then routed by
[`scripts/process_triage_actions.py`](scripts/process_triage_actions.py)
to the appropriate side file based on the user's `action_to_take`
column:

| action | destination | role |
|---|---|---|
| `add_event` | [`data/triage_events.csv`](data/triage_events.csv) | new annotations event, merged into annotations.yaml |
| `add_to_context` | [`data/per_day_extra_context.csv`](data/per_day_extra_context.csv) | extra context for the day; not a standalone event |
| `mark_dip` | [`data/sub_threshold_dips.csv`](data/sub_threshold_dips.csv) | user self-identifies a sub-threshold dip (score > 3 but crash-like symptoms) |
| `refine_tags` | [`data/v2_tag_refinements_queue.csv`](data/v2_tag_refinements_queue.csv) | flagged for future v2 categorisation refinement |
| (empty) | source CSV stays as-is | no structured action; note remains searchable in per_day_intensity_YYYY.csv |

The four side files are **structured complements** to the per-day
database:

- `triage_events.csv` extends `annotations.yaml` (operationally
  consumed by the timeline render)
- `per_day_extra_context.csv` extends `day_entries.note` (consumed by
  qualitative sensemaking)
- `sub_threshold_dips.csv` extends `labels_crash_v2.csv` (consumed by
  statistical analyses that want to include self-identified dips)
- `v2_tag_refinements_queue.csv` feeds the future v2 categorisation
  refinement round

### 2d. per_day_intensity.csv format


```
date,cog,phy,emo,source,notes
2024-03-04,2,,,consolidation_2026-06-10,
2024-06-23,2,1,,consolidation_2026-06-10,
...
```

Columns:
- `date`: ISO date
- `cog`, `phy`, `emo`: 1-3 or blank (the unified per-day value)
- `source`: where this row came from (e.g.
  `consolidation_2026-06-10`, `per_year_triage_2024`, etc.)
- `notes`: user context, including explicit-blank annotations like
  "no specific loads needed on this day"

The file is appended to as triage rounds complete. Existing rows are
updated, not duplicated, when re-triaged.

## 3. Two kinds of content in notes

Day-entry notes typically contain a mix of two content types:

| type | example | how to handle |
|---|---|---|
| **Factual event** | "Naar mat en annel, was teveel van het goede" | candidate for a timeline event; label = event (the social evening), loads = intensity of the event |
| **Pacing reflection** | "Denk dat ik vandaag te veel heb gedaan" | not a timeline event on its own; goes into the `notes` column of the related event, or stays in the source CSV as descriptive context |
| **Pure state of being** | "Erg moe einde dag" (no trigger named) | usually skipped (`n` or blank); the score on that day already captures the state |

Pacing reflections often contain valuable hindsight ("third time after
X that I crash"). They are preserved in the source CSV as is. When a
factual event is added to the timeline, any pacing reflection in the
same note can be quoted into the `notes` column for traceability.

## 3a. Symptom-mention asymmetry (interpretation rule)

Day-entry notes are written by the user as free-form reflection, not as a
structured symptom log. This makes symptom mentions in notes **inconsistent
in coverage but reliable in presence**:

- When a symptom is **mentioned**, it was experienced that day. The note
  is a positive record.
- When a symptom is **not mentioned**, we cannot conclude it was absent.
  It may simply not have crossed the threshold for being worth writing
  down, or another topic crowded it out.

This asymmetry has direct implications for analysis. Two symptom families
in particular are worth treating as **hypothesis-generating signals**
rather than reliable trackers:

### Brainfog mentions on score-4 days

Phrases like `brainfog`, `duf hoofd`, `wazig hoofd`, `vergeetachtig`,
`niet helder` appearing on a day with `gevoelscore = 4` are likely
indicators of a **sub-threshold dip without somatic pain**. The
hypothesis: the score sits at 4 (not 5) precisely because brainfog is
keeping the cognitive system from registering "normal", even though
nothing physically hurts. These days deserve to be considered
**candidate dips** in any push-crash analysis, even though
[`labels_crash_v2.csv`](../garmin/hypotheses/crash_v2-definition/labels_crash_v2.csv)
typically only labels score ≤ 3.

This is captured operationally by routing such mentions to
[`data/sub_threshold_dips.csv`](data/sub_threshold_dips.csv) during
triage (via `mark_dip` action, see §2c).

### Muscle-pain mentions as potential crash precursors

Phrases like `spierpijn`, `zere benen`, `zwaar in de benen`, `dof gevoel`
are similarly underreported in the same way as brainfog. But when they
**do** appear, the working hypothesis is that they **may precede or
coincide with a crash or dip** in the following 1-3 days, even if the
score on the mention-day itself is unremarkable.

This is testable: extract all dates where muscle-pain language appears
in the note, then check whether the gevoelscore trajectory in the next
72 hours differs significantly from a matched control sample of mention-
free days. A positive result would make muscle-pain mentions a useful
forward-looking marker, even with their incomplete coverage.

### Why these two specifically

Both brainfog and muscle-pain share three properties:
1. They are part of the canonical PEM / PAIS symptom cluster.
2. They are unevenly reported in notes (asymmetry confirmed during
   v2 categorisation rounds).
3. Their underlying physiological mechanism (autonomic + metabolic
   dysregulation) is exactly the territory the Garmin biometric layer
   may pick up — making cross-modal validation possible.

The interpretation rule for triage and downstream analysis:

> Treat presence of a symptom mention as a high-specificity (low-
> sensitivity) positive signal. Never treat absence as evidence that
> the symptom was not there.

## 3b. Objective data sources for cross-validation

The per-day intensity vectors are codifications of the user's notes and
calendar memory. They are the best signal we have for cog/phy/emo loads,
but they are still **retrospective and subjective**: each load value
represents the user's judgement at triage time, not an instrument
reading.

When **objective per-day records** exist from external systems, they
can be used as a **cross-validation layer** — surfacing days where the
objective record and the user's retrospective triage disagree. Disagreement
is not failure of either source; it is the most useful pointer to where
the triage may have missed something.

### First-class objective source: PwC reintegration daily log

Added 2026-06-11. The user's original `Reintegratie Willem.xlsx`
(maintained between 2022-09-26 and 2024-02-26 during the LC
reintegration period at PwC) contains:

- daily primary work hours (the planned reintegration hours)
- daily secondary hours (travel / meetings / admin)
- free-text toelichting per day (note on what was done, who was met,
  any illness)

Parsed by
[`scripts/parse_reintegration_hours.py`](scripts/parse_reintegration_hours.py)
into
[`data/reintegration_hours_2022-2024.csv`](data/reintegration_hours_2022-2024.csv)
with one row per day, columns:

```
date, week, primary_hours, secondary_hours, total_hours,
illness_flag, doctor_visit_flag, amsterdam_flag, vacation_flag,
source_tab, toelichting
```

The boolean flags are derived from toelichting text via simple regex
(`ziek`, `bedrijfsarts`, `naar amsterdam`, `vakantie`, etc.). They are
**indicative, not exhaustive** — a day flagged `illness_flag=0` may
still have been a difficult day if the user simply did not write
"ziek" in the toelichting.

### Cross-validation method

[`scripts/cross_validate_with_intensity.py`](scripts/cross_validate_with_intensity.py)
compares the objective PwC log against three existing sources:

| comparison | objective signal | existing signal | output |
|---|---|---|---|
| Illness stretches | `illness_flag = 1` for ≥3 consecutive days | dip/crash labels in `labels_crash_v2.csv` + `sub_threshold_dips.csv` | gap if overlap < 50% |
| Work-heavy days | `total_hours ≥ 4` | any cog/phy/emo load in `per_day_intensity.csv` | gap if no load assigned |
| Doctor visits | `doctor_visit_flag = 1` | medical span in `annotations.yaml` covering the date | gap if no medical span |

Output: [`data/reintegration_gaps.csv`](data/reintegration_gaps.csv) with
columns `gap_type, date_start, date_end, length, needs_review, context,
overlap_with_existing` — one row per gap, sorted by date. The
`needs_review` column is the user's review surface (same workflow as
the per-year triage rounds): user inspects, decides whether to add to
`triage_events.csv` / `sub_threshold_dips.csv` / per_day_intensity, or
leaves the gap unresolved (e.g., "this was a regular cold, not a PEM
dip").

### What cross-validation is and is not

- **Is**: a quality-control surface — points at days the retrospective
  triage may have missed because the objective record contradicts it.
- **Is not**: a re-triage script. It does not auto-update annotations
  or per_day_intensity. The user reviews each gap and decides.

### What "validation" means here (important interpretive lens)

The PwC reintegration log and dossier records measure
**work-incapacity** ("kon de gebruiker werken op die dag, en zo ja,
hoeveel uur"). The gevoelscore measures **subjective state** ("hoe
voelde de gebruiker zich"). **These two constructs are always
distinct.** Even when the user allocates nearly all available energy
to work, "ziek voor werk" still measures something different than
"PEM-crash" — one captures incapacity to perform an external task,
the other captures internal experience. They correlate, often
strongly, but they never map 1-1.

This was crisply demonstrated by the user's decision during dossier
review (2026-06-11) to label the 16-day "volledig ziek" period of
June 2023 as `levensgebeurtenis` (NOT `crash`), explicitly noting
"not a crash but this is context dont read it as medical physical
information". June 2023 fell deep inside the "all-energy-to-work"
period when one might naively expect work-incapacity ≈ PEM-crash;
the user's own retrospective judgement rejected that equivalence.
The two constructs were distinct then too.

**Implication for cross-validation:** disagreement between the dossier
"ziek" record and the gevoelscore crash labels at any time is **not a
sign that one source is wrong**. It is a sign that the two sources are
measuring two related-but-distinct phenomena. The job of cross-
validation is not to force the sources to agree, but to surface where
they disagree and ask **why**.

### Qualitative context: a gradual shift in personal energy-allocation

Around late 2023, the user's personal strategy for allocating limited
energy gradually shifted from "almost all available energy goes to
work and reintegration" to "energy split between work, family, and
active recovery", as the realisation of chronic illness set in. The
2023-10-09 SMB-consult ("20u/wk = plafond, no more building up")
formally registered the end of the recovery-toward-AD-target plan;
the 2023-12-08 "extra event" accelerated the practical shift.

This shift is **qualitative context**, not a discrete timeline event.
It does not have crisp start or end dates — it was a gradual change in
internal priority over weeks to months. It is documented here in the
methodology for interpretive use, but it is **not** added as a span
on the timeline (an earlier draft did add it as an umbrella span; it
was removed on 2026-06-11 because a span misrepresents a continuous
qualitative change as a discrete event).

The shift matters for reading the PwC log post-2023-10 carefully:

- **What it changes**: an absent work-hour in the post-shift period
  may reflect a priority choice (the user could have worked but chose
  to spend energy elsewhere) rather than incapacity. Reading post-shift
  zero-hour days as "ziek" risks overcounting.
- **What it does NOT change**: the underlying truth that work-data
  and state-data measure two different constructs. That truth held
  before the shift and holds after it.

### Implication for future objective sources

This lens applies to every future objective source we integrate:
training-load logs from Garmin, sleep windows, etc. They all measure
*something specific* (work hours, training intensity, recovery time),
which is structurally distinct from subjective state. Expect them to
correlate where the user's energy-allocation concentrates the
measured behaviour into the measured construct (e.g. all-to-training
during a build period); expect them to diverge otherwise. Neither
direction is failure of the data — it is the signal.

### Findings from the first cross-validation pass (2026-06-11)

The PwC reintegration log was the first objective source compared
against the per-day database. Result: **the objective record largely
confirms the existing retrospective triage on safety-relevant macro
signals**, with the work-vs-subjective-state caveat above.

- **Illness stretches** (`illness_flag = 1` for ≥3 consecutive days):
  4 stretches in the PwC log, of which 3 have **100% overlap** with
  `labels_crash_v2.csv` dips/crashes + `sub_threshold_dips.csv`, and
  the 4th has 3 of 4 days overlapping. Conclusion: the combination of
  research-derived crash_v2 labels + user retrospective dip-triage
  catches the multi-day illness periods that the objective record also
  marks. The two sources are corroborative, not contradictory — within
  the early-reintegration period when the work-vs-subjective-state
  mapping was approximately 1-1. The dossier (with the deeper June 2023
  and January 2024 records) is reviewed under the same interpretive
  lens.
- **Work-heavy days without cog_load** (21 days): the cog_load column
  in per_day_intensity is under-attributed for high-hours days during
  the reintegration period. Not surprising — during the bulk per-day
  intensity triage rounds the user worked from notes + calendar, and
  the PwC log was not yet consulted. These 21 days are clear
  candidates for adding cog_load.
- **Doctor visits not in annotations** (12 days): bedrijfsarts /
  casemanager / huisarts / ergotherapeut visits — the medical category
  in `annotations.yaml` is currently sparse for the reintegration
  period.

The two material gaps (cog_load on work-heavy days, missing medical
visits) reflect blind spots in the retrospective triage, not errors in
the methodology. They are addressable by user review of
[`data/reintegration_gaps.csv`](data/reintegration_gaps.csv) and
re-running the standard mergers.

**Implication for future objective sources**: when a similar objective
log (Garmin training-load, Garmin sleep, etc.) is integrated, expect a
similar pattern — high agreement on safety-relevant macro-signals
(illness, crashes), real gap-filling value on under-attributed
day-level cog/phy/emo loads, and a long-tail of small annotation
additions (visits, single-day events) that the retrospective triage
naturally misses.

### Adding additional objective sources

The same pattern (parse → cross-validate → gaps file for user review)
is the canonical way to integrate any future objective per-day log
(Garmin training-load extracts, Garmin sleep windows, calendar
exports from other employers, etc.). Each new source should:

1. Live as its own `data/<source>_<years>.csv`.
2. Have its own `parse_<source>.py` script.
3. Extend `cross_validate_with_intensity.py` (or live in a sibling
   `cross_validate_<source>.py`) so gaps are surfaced as the same
   `reintegration_gaps.csv`-style review file.
4. Be added to the source table in §0 above.

## 4. Event-label conventions

Labels describe **what happened** (the event), not **how the user
felt afterwards** (the after-effect). When the after-effect is
material context the label adds a parenthetical hint, but the
primary label is the event.

| pattern | template | example |
|---|---|---|
| Direct event | `[name of event]` | "Bestuursweekend" |
| Event with consequence hint | `[event] ([consequence])` | "Wandeling 15 min (terugslag)" |
| Multi-day umbrella | `[name of period] (umbrella)` | "Mirjam-periode (Angela tensions + relatiecoach met Jantine)" |
| Treatment / intervention | `[Trial name] - [optional phase]` | "Citalopram fase 3: 30mg plateau" |
| PEM-style delayed crash | `PEM-respons na [trigger or period]` | "PEM-respons na Mirjam-sessie" |

When in doubt, prefer **shorter, factual labels** over expressive
ones. The timeline visualisation truncates long labels and the user
can always click through to the source `note` column for detail.

## 5. Category assignment

The `category` column selects the visual band colour on the timeline.
The default mapping when a row is marked `y` and `category` is left
blank:

| max load value | default category | when to override |
|---|---|---|
| any axis = 3 | `high_intensity` | override to `interventie` for treatments (e.g. citalopram phase) or `medical` for one-off visits (e.g. huisarts with high emo) |
| max axis = 2 | `levensgebeurtenis` | override to `medical` for any medical visit |
| max axis = 1 | `levensgebeurtenis` | rarely override |
| all blank | `levensgebeurtenis` for events, `medical` for medical-topic notes | use the topic-default; override only when clear |

Special categories:

- **`trigger`**: only for the corona infection (the single causal
  trigger event for long COVID onset).
- **`marker`** (single-day): used for one-off milestone moments like
  the LC diagnose. Markers render as triangles in their own row.

## 6. Decision rules per row

Before marking `y`, check the **`existing_on_day` column** (added by
[`enrich_notes_with_existing.py`](scripts/enrich_notes_with_existing.py)).
This column lists every research crash / dip, every prior y-marked
event with its loads, and every umbrella span covering that date.
It is the canonical "what's already there" lookup.

Then ask, in order:

1. **Is the event already on the timeline?**
   - `existing_on_day` shows a matching label? → leave blank.
   - `existing_on_day` shows `CRASH` or `DIP`? → leave blank unless
     the note describes a specific trigger that explains the crash
     and isn't named elsewhere.
   - `existing_on_day` shows an umbrella span that covers the same
     theme? → leave blank unless this specific day adds value
     (e.g., a particularly intense session within a long coaching
     period). Umbrellas are tagged ` (umbrella)` in the column.

2. **Does the day already have loads assigned from another triage row?**
   - `existing_on_day` shows entries like `Bestuursweekend [c3/p3/e3]`?
     → those loads belong to that event. You can add new loads for a
     **different** event on the same day, but make sure the labels
     describe distinct events so the timeline does not double-count.

3. **Does the note describe a specific event, or only a state?**
   - Specific event → `y`.
   - Only state ("moe einde dag" without trigger) → leave blank.

4. **Does the event add context for future research?**
   - Yes → `y` with full labels and loads.
   - No (too generic) → leave blank.

When in doubt, **leave blank**. Source data is preserved either way.

## 7. Source-of-truth principles

- The CSV file on disk is the source of truth for every triage round.
  The merger reads it; it never deletes or rewrites the CSV.
- Rows with `keep_yn` empty or `n` stay in the CSV with their
  `note_full`, `score`, and `matched_keyword` columns intact. They
  remain available for ad-hoc lookup, future re-triage, or other
  downstream analyses.
- The `merge_*_triage.py` scripts are idempotent. Re-running them
  produces the same `annotations.yaml` for the same CSV state.

## 8. Workflow ordering

Re-running mergers in the right order matters because
`merge_calendar_triage.py` rewrites `annotations.yaml` from scratch
(hand-curated entries + calendar CSVs), while `merge_notes_triage.py`
appends to the existing file.

The canonical sequence after any source change is:

1. `python merge_calendar_triage.py` — rebuilds annotations base.
2. `python merge_notes_triage.py` — adds notes-derived entries on top.
3. `python build_timeline.py` — renders the picture.

If only notes CSVs changed and `merge_calendar_triage.py` has not
been re-run, step 1 can be skipped.

## 9. Hand-curated entries

Entries that cannot be derived from calendar or notes (because they
were not logged, or fall outside calendar coverage) live in
`merge_calendar_triage.py` as `HAND_CURATED_*` lists. Examples:

- Training period before LC (2021-08-16 → 2022-03-22), derived from
  the activities.csv workout density.
- Corona infection (2022-03-23 → 2022-03-30), reconstructed from
  the gap in training activity (week 12).
- CPAP intervention (2024-01-10 → 2024-02-28), reconstructed from
  day-entry notes.
- Citalopram dose phases (6 sub-spans + umbrella), reconstructed
  from day-entry notes.
- Umbrella narrative periods (Mirjam, Werk-transitie, etc.),
  reconstructed from user-provided context.

Hand-curated entries are the **least traceable** annotations and
should be the **first** to be revised when better source data
becomes available.

## 10. Anti-patterns to avoid

- **Marking every keyword hit `y`.** The CSVs are keyword-extracted
  candidates, not curated event lists. Many keyword matches are
  false positives or duplications of timeline content. The triage
  is the filter.
- **Using 1-3 to mean different things in different sheets.** The
  scale is locked across all sources. See §2.
- **Letting after-effects bleed into load values.** Loads describe
  the event. After-effects (crashes, fatigue, hangover days) are
  separate phenomena.
- **Renaming labels mid-round to be more descriptive.** Consistency
  beats variety. If a category truly needs a new label convention,
  update §4 first, then apply.
- **Adding umbrella spans without checking overlap with existing
  ones.** Umbrellas serve as background context; stacking too many
  reduces visual clarity. Aim for at most 2-3 concurrent umbrellas
  per period.

## 11. Methodology history

- **2026-06-08**: Initial triage workflow established with calendar
  CSVs, the `keep_yn` + per-event 1-3 load model adopted.
- **2026-06-09**: Topic-targeted notes extraction added
  (`extract_notes_candidates.py`) for medical, overload, events.
- **2026-06-10**: The 1-3 load scale locked as "event intensity, not
  after-effect severity" after an inconsistency surfaced in an
  overload-labeling suggestion. Factual-vs-reflective content
  distinction made explicit (§3). Decision rules per row written
  down (§6).
- **2026-06-10** (later): `existing_on_day` column added to notes
  triage CSVs via
  [`enrich_notes_with_existing.py`](scripts/enrich_notes_with_existing.py).
  Surfaces research crashes/dips + every prior y-marked event with
  its loads + umbrella spans. Prevents duplicate event-entries and
  double-scored days. Decision rules §6 updated to require checking
  this column before marking `y`.
- **2026-06-10** (later still 2): per-event vs per-day load
  distinction locked in §2a. Audit script
  [`audit_annotations.py`](scripts/audit_annotations.py) identified
  21 multi-load conflict days needing manual consolidation. Decision:
  per-event loads are preserved as descriptive metadata; per-day
  unified loads will live in a separate per-day intensity layer.
  MAX-aggregation rejected because two cog=2 events may be
  experienced as cog=3 cumulatively or remain cog=2 if recoverable;
  only the user can decide.
- **2026-06-10** (later still 3): user triaged the 21 consolidation
  days; results saved to
  [`data/per_day_intensity.csv`](data/per_day_intensity.csv) (12
  with loads + 9 explicit-blanks annotated "no specific loads
  needed"). Multi-day-span rule articulated and locked in §2b:
  loads are stripped from multi-day events in both mergers so a
  generic event-level rating does not leak into per-day intensity.
  Audit count of multi-load events dropped from 153 to 117, and
  multi-load conflict days dropped from 21 to 9 (the remaining 9
  are legitimately distinct single-day events already covered by
  per_day_intensity.csv).
- **2026-06-10** (later still 4): 2026 bulk per-day intensity triage
  completed (243 rows merged into master). Triage notes processed
  via classifier + action-router into four side files: 12 events
  added to annotations via `triage_events.csv`, 9 day-context
  entries to `per_day_extra_context.csv`, 3 self-identified dips
  to `sub_threshold_dips.csv`, 2 v2-tag-refinement queue items to
  `v2_tag_refinements_queue.csv`. New methodology §2c articulates
  the four complementary side-files as structured extensions of
  the per-day database.
- **2026-06-10** (later still): strategic frame articulated in §0.
  Clarified that this is a per-day contextual database supporting
  both statistical (gevoelscore + planned intensity vectors) and
  qualitative (events, episodes, key moments) analyses. The
  rendered `output/timeline.png` is a verification tool, not the
  product. Triage decisions are about structuring data, not judging
  importance — generic state-of-being notes stay in the source
  notes-text record either way.
- **2026-06-11**: 2024 bulk per-day intensity triage completed (366
  days reviewed: 129 with loads, 234 notes-only, 3 truly-empty
  marked `bulk_triage_2024_no_info`). 41 new add_event entries; 7
  new sub-threshold dips. Six multi-day clusters consolidated
  manually (bestuursweekend, tuinfeest, jantine ill, weekendje
  amsterdam, opruimactie schuur, münster trip).
  [`process_triage_actions.py`](scripts/process_triage_actions.py)
  bug fixed: dedupe key changed from `date_start` to
  `(date_start, label)` so re-runs no longer wipe manual entries
  that share a date with auto-detected events. Inline action
  patterns expanded to catch `dip day`, `add events` (plural),
  `add multi day event`, `add devent` (typo).
- **2026-06-11** (later): timeline rendering layer expanded.
  [`build_timeline.py`](scripts/build_timeline.py) now reads
  [`data/per_day_intensity.csv`](data/per_day_intensity.csv) and
  [`data/sub_threshold_dips.csv`](data/sub_threshold_dips.csv) and
  renders three heatstripes (cog blue / phy orange / emo purple)
  underneath the gevoelscore line + down-pointing triangle markers
  for user-triaged sub-threshold dips on the score line. Plan
  decisions locked: skip per-day extra context on the static PNG
  (it lives in side files for qualitative use); defer medicatie
  per-day strip; build an interactive HTML timeline as a separate
  follow-up artefact rather than expanding the PNG further.
- **2026-06-11** (later): strategic frame refined in §0 to make
  explicit that the per-day intensity vectors **codify** existing
  notes + calendar content rather than collecting new data. The
  vectors therefore inherit the source material's coverage gaps,
  which motivates the new §3a on symptom-mention asymmetry:
  brainfog mentions on score-4 days are candidate hidden dips, and
  muscle-pain mentions may be testable crash precursors. Both
  remain hypothesis-generating signals, not reliable trackers.
- **2026-06-11** (later): 2023 + 2022 per-day intensity triage rounds
  shipped. 2023: 365 days reviewed (100 with loads, 4 add_to_context, 39
  add_event including 3 multi-day clusters: pinksterweekend, klustival
  Zuna jun, in Zuna dec); BOILERPLATE pattern extended to catch
  `no data that signifies load`. PwC reintegratie 2023 umbrella span
  added (2023-03-06 → 2023-11-28) over 8 individual Amsterdam visits.
  2022: 305 days reviewed (21 with loads, 5 add_to_context, 9 add_event
  including the consolidated 8-day "jantine in caribbean voor werk"
  span 2022-10-20 → 2022-10-27); BOILERPLATE extended again to catch
  `no additional load data`. Final corpus: 1644 entries in
  per_day_intensity.csv, 130 events in triage_events.csv, 465 spans
  in annotations.yaml. Full 2022-09-03 → 2026-06-10 score corpus is
  now reviewed.
- **2026-06-11** (later still): objective cross-validation layer added
  in §3b. PwC reintegration daily-hours log (2022-09-26 → 2024-02-26,
  239 days) parsed into
  [`data/reintegration_hours_2022-2024.csv`](data/reintegration_hours_2022-2024.csv).
  Cross-validation script
  [`scripts/cross_validate_with_intensity.py`](scripts/cross_validate_with_intensity.py)
  surfaced **37 gaps**: 4 illness stretches (most overlap with existing
  dip/crash labels — reassuring agreement between objective record and
  user triage), 21 work-heavy days (≥ 4h) without cog_load in
  per_day_intensity, and 12 doctor visits not yet in annotations.
  Gaps written to
  [`data/reintegration_gaps.csv`](data/reintegration_gaps.csv) for user
  review (same workflow as triage rounds).
- **2026-06-11** (later still): user-triaged dispatch of both review
  files. **Reintegration gaps** (37 rows, gap-cross-validation):
  4 mark_dip on illness stretches, 12 add_event (7 medical + 5 "naar
  amsterdam PwC reintegratie" levensgebeurtenis), 21 add_cog_load,
  5 add_phy_load (Amsterdam-PwC compound rows), 5 skip. **PwC dossier**
  (53 rows): 28 keep + 25 drop/skip. Of the 28 kept: 15 medical
  bedrijfsarts/casemanager/spoor_2 visits, 10 levensgebeurtenis context
  spans, 3 marker milestones. Critical decision: the 16-day June 2023
  "volledig ziek" period was kept as `levensgebeurtenis` (NOT `crash`),
  because the user labelled it "not a crash but this is context dont
  read it as medical physical information". This is the empirical
  confirmation of the work-vs-state distinction now anchored in §3b.
  After both dispatches: annotations.yaml has 505 spans (was 465), of
  which 25 medical (was 3).
- **2026-06-11** (later): Q3b umbrella-review for 2024+2025 completed.
  Keyword-clustering surfaced 15 candidate clusters; 1 actioned: new
  umbrella `Angela-spanning 2024 (umbrella)` 2024-06-06 → 2024-11-24,
  category `levensgebeurtenis`, source `q3b_umbrella_review_2026-06-11`.
  Other 14 clusters rejected as either family-name aggregation (Jantine,
  Tijmen, Tobias), generic activity-type recurrence (sailing, koffie,
  eten), or broad-category aggregation (kids, gezin). The 1-umbrella
  conservative outcome respects methodology §4's "at most 2-3 concurrent
  umbrellas per period" guideline. annotations.yaml: 506 spans (was
  505).
- **2026-06-11** (later): Q2 hidden-dip review partial completion. The
  29 quasi_crash_context candidates (after excluding already-labeled
  dates) were reviewed. The user added 8 with explicit brainfog
  mentions to [`data/sub_threshold_dips.csv`](data/sub_threshold_dips.csv)
  with new `dip_type=brainfog` column (training labels for the §3a
  brainfog-hidden-dip hypothesis). The 21 remaining candidates without
  explicit brainfog mention were explicitly skipped per conservative
  user choice — only solid symptom-mention signals enter the training
  set; ambiguous "moe / groggy" days stay in source data for ad-hoc
  lookup but do not feed downstream analysis. A new `dip_type` column
  was added to sub_threshold_dips.csv (values: `general` for the prior
  27 entries, `brainfog` for the 8 new). The schema extension makes
  the §3a hypothesis testable by filtering on dip_type. Total
  sub_threshold_dips.csv: 35 entries (27 general + 8 brainfog).
- **2026-06-11** (later, then walked back): Q3a from queued_work was
  briefly shipped as an umbrella span 2023-10-09 → 2023-12-08 with the
  label "Energie-allocatie shift". §3b initially framed the shift as
  an interpretive regime-grens where "before the span, work-incapacity
  ≈ PEM-crash; after it, the two diverge". User pushed back on the
  framing during the same session: the work-vs-state distinction was
  always there (the June 2023 decision proved it), so the shift cannot
  be the regime boundary. The shift is also gradual and lacks crisp
  dates, so treating it as a discrete span misrepresents it. The span
  was removed from `triage_events.csv` the same day. The qualitative
  context is preserved in §3b under "Qualitative context: a gradual
  shift in personal energy-allocation". annotations.yaml: back to 505
  spans (the dossier dispatch additions remain).
- **(future)**: Q1 (formal HA-pre-registration of brainfog-hidden-dip
  and muscle-pain-crash-precursor hypotheses), Q2 (hidden-dip review on
  the 88 quasi_crash_context days across 2022-2025), Q3b (umbrella-span
  review for 2024 + 2025), Q5 (cross-validation lens guidance for next
  objective source) — see [`queued_work.md`](queued_work.md) for status
  and triggers.

## 12. Cross-references

- [`README.md`](README.md): data sources, file layout, data-quality
  caveats.
- [`queued_work.md`](queued_work.md): research follow-ups deferred from
  triage sessions — formal HA-pre-registration for §3a hypotheses,
  hidden-dip review of quasi_crash_context days, umbrella-span review
  for 2024+2025.
- [`data/annotations.example.yaml`](data/annotations.example.yaml):
  example annotation entries.
- [`scripts/merge_calendar_triage.py`](scripts/merge_calendar_triage.py):
  calendar merger + hand-curated entries.
- [`scripts/merge_notes_triage.py`](scripts/merge_notes_triage.py):
  notes merger.
- [`scripts/extract_notes_candidates.py`](scripts/extract_notes_candidates.py):
  topic-targeted note extraction.
- [`scripts/export_calendar_triage.mjs`](scripts/export_calendar_triage.mjs):
  calendar event extraction with pre-fill of prior-round rejections.
- [`scripts/enrich_notes_with_existing.py`](scripts/enrich_notes_with_existing.py):
  adds `existing_on_day` column to notes triage CSVs (research labels +
  prior y-marked events with loads + umbrella spans).
- [`scripts/audit_annotations.py`](scripts/audit_annotations.py):
  audits annotations.yaml for exact duplicates, same-day event
  clusters, multi-load conflict days, and umbrella-vs-nested overlap.
  Run after any merger update to verify the database is clean.
- [`scripts/parse_reintegration_hours.py`](scripts/parse_reintegration_hours.py):
  parses the PwC reintegration daily-log spreadsheet into
  [`data/reintegration_hours_2022-2024.csv`](data/reintegration_hours_2022-2024.csv)
  with flags for illness/doctor/amsterdam/vacation. See §3b for cross-
  validation workflow.
- [`scripts/cross_validate_with_intensity.py`](scripts/cross_validate_with_intensity.py):
  cross-validates the PwC log against per_day_intensity, dip/crash
  labels, and medical annotations. Surfaces gaps in
  [`data/reintegration_gaps.csv`](data/reintegration_gaps.csv) for
  user review.

---

*Working document. Update with each new triage round or calibration
decision.*
