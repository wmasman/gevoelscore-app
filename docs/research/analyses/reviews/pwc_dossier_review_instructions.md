# How to triage `pwc_dossier_review.csv`

53 dossier entries to review per-entry. The mapping (dossier category +
type → annotations category) has been pre-applied as a **suggestion**.
You confirm, override, or skip per row.

## Workflow

1. Upload [`data/pwc_dossier_review.csv`](pwc_dossier_review.csv) to a
   new Google Sheet.
2. For each row, fill the `action_to_take` column with one of:
   - `accept` — use suggested category and label as-is (most common)
   - `skip` — do not add this entry to annotations (e.g. duplicate of
     a span we already have, or you decide it's not material)
   - `change_category:CATEGORY` — override the suggested annotations
     category (use a name from the standard palette: `crash`, `dip`,
     `high_intensity`, `levensgebeurtenis`, `medical`, `interventie`,
     `trigger`, `marker`)
   - `change_label:LABEL` — override the dossier title with a cleaner
     event label (the dossier title is sometimes too document-flavored;
     short labels render better on the timeline)
3. Optionally also fill `user_label_override` (a shorter label) and
   `user_notes` (context for future-you).
4. Share the Sheet link back; the pipeline picks it up.

## What the columns mean

| column | what it shows | who fills |
|---|---|---|
| `date_start`, `date_end` | dossier date(s) | dossier |
| `multi_day` | `yes` if span, `no` if single day | dossier |
| `date_precision` | `day` (hard) / `month` (approx) / `week` | dossier |
| `dossier_category` | original dossier classification | dossier |
| `dossier_type` | original dossier type (e.g. `crash_period`, `consult`) | dossier |
| `title` | original dossier title | dossier |
| `person` | who was involved (bedrijfsarts name etc.) | dossier |
| `source_pdf` | which PDF this came from | dossier |
| `suggested_annotations_category` | proposed timeline category | mapping |
| `suggested_action` | `accept` (default) or `skip` (redundant entries) | mapping |
| `action_to_take` | YOUR decision | YOU |
| `user_label_override` | optional shorter label | YOU |
| `user_notes` | your reasoning | YOU |
| `dossier_notes` | first 200 chars of dossier note | dossier |

## Pre-applied mapping

| dossier (category/type) | → annotations category | reason |
|---|---|---|
| `health_event` + `crash_period` | `crash` | hard medical crash evidence (multi-day uitval) |
| `health_event` + `crash` / `terugslag` | `crash` / `dip` | single-day crash events |
| `health_event` + `terugval` | `dip` | "terugval" is often month-precision; dip is safer |
| `health_event` + `first_episode` | `high_intensity` | initial illness, not yet LC-classified |
| `health_event` + `onset` / `uitval` / `herstart` / `opbouw` | `marker` | milestone moments |
| `bedrijfsarts` + (any) | `medical` | all bedrijfsarts consults are medical events |
| `arbeidsdeskundig` + `onderzoek` / `rapportage` | `medical` | substantive medical assessments |
| `arbeidsdeskundig` + `opbouwschema` | `interventie` | multi-day treatment trajectory |
| `pwc_intern` + `meeting` / `contact` / `actie` | `levensgebeurtenis` | reintegratie context |
| `pwc_intern` + `milestone` | `marker` | werkhervatting moments |
| `pwc_intern` + `vakantie` / `wachttijd_loondoorbetaling` | `levensgebeurtenis` | context spans |
| `spoor_2` + `intake` / `sessie` | `medical` | individual sessions |
| `spoor_2` + `trajectduur` | `interventie` | parallel treatment trajectory |
| `spoor_2` + `ziekmelding` | `dip` | active worsening within trajectory |
| `uwv` + `upload` | `marker` | admin milestone |

## Pre-skipped rows

These 5 dossier entries are NOT in the review file (pre-filtered as
paper-trail-only, per our earlier decision):

- 2022-08-10: Plan van aanpak ondertekend
- 2022-09-28: Probleemanalyse document (signature)
- 2023-08-14: Eerstejaarsevaluatie ondertekend
- 2024-01-23: Eindevaluatie opgesteld (document creation)
- 2024-01-29: Eindevaluatie ondertekend

If you want any of these back as markers, let me know and I'll re-emit.

## Critical interpretive lens before triaging

**Dossier "crash"/"ziek" entries describe WORK-INCAPACITY, not your
subjective state.** The dossier was written from PwC + Arbo Unie
perspective: "could the user work that day, and how many hours". This
is related to but distinct from how the user actually felt.

This distinction matters during triage because the two crash periods
in the dossier fall on opposite sides of an important boundary:

**Boundary**: roughly October-November 2023, the user reallocated
energy from "all to work" to "split with family + active recovery"
as the chronic-illness realisation set in. The "extra event" on
2023-12-08 marks the formal acceleration of this shift.

| dossier crash period | timing relative to boundary | interpretation |
|---|---|---|
| 2023-06-05 → 2023-06-21 (16d) | **before** boundary (all-to-work) | work-incapacity ≈ PEM-crash. Map to `crash`. |
| 2024-01-02 → 2024-01-08 (7d) | **after** boundary (rebalanced) | work-incapacity ≠ PEM-crash necessarily. May still be a crash, but check against gevoelscore. Could also be `dip` or `interventie`. |

When you triage the dossier rows:

1. **June 2023 crash_period**: default `accept` (maps to `crash`) — the
   work-vs-state correspondence is good in this window.
2. **January 2024 crash_period**: review more carefully. If the
   gevoelscore on those days actually dropped to crash-level (≤3), keep
   as `crash`. If it stayed at dip-level (4) despite the "volledig
   uitgevallen" work label, override to `change_category:dip`. If the
   user actively chose to not work but felt OK, possibly `skip`.

Use the same lens for:

- Monthly-precision `terugval` entries (suggested `dip`). The dossier
  notes these as "datum onbekend" — the work-incapacity-vs-state
  ambiguity is even larger here. `change_label` to add the uncertainty
  is fine.
- All bedrijfsarts consults (suggested `medical`). These are objective
  events regardless of state, so the lens doesn't apply.

## What to look out for

### Crash period vs crash_start/end pairs

The two crash periods in the dossier are entered both as a span
(`crash_period`) AND as paired single-day markers (`crash_start` +
`crash_end`):

- 2023-06-05 → 2023-06-21 (16-dag uitval juni)
- 2024-01-02 → 2024-01-08 (7-dag uitval januari)

The paired single-day markers (`crash_start`/`crash_end`) are
suggested `skip` by default since the span already covers them. You
can override if you want both.

### Monthly-precision terugval rows

3 rows have `date_precision: month` (datum onbekend, monthly approx):

- 2022-09-01: Terugval (gerapporteerd 21-09)
- 2023-09-01: Terugval na zomer 2023
- 2023-11-01: Structurele terugval vanaf november 2023

These are mapped to `dip` (single-day) at the month's first day. The
actual date is uncertain. You may want to skip these (since we don't
know the date precisely) OR change the label to make the uncertainty
explicit (e.g. "Terugval ergens sept 2023 — datum onbekend").

### The 104-week umbrella

The `wachttijd_loondoorbetaling` row spans 2022-04-25 → 2024-04-17
(24 months). On the timeline this would be a long levensgebeurtenis
band across the entire reintegration period. Probably the most
information-dense single annotation we have. Default: `accept`.

### Bedrijfsarts cluster overlap

13 bedrijfsarts consults are in the dossier. None are currently in our
medical annotations. If you `accept` all 13, the timeline gets 13 new
medical-colored markers in 2022-2024 — that's a lot of visual density
but it's the truth. Consider:

- `accept` all (full medical record)
- Selectively `skip` the brief telefonisch-only consults

## Expected effort

~45 min for 53 rows. Most rows resolve in seconds via `accept`. The
attention is on:

- 3 crash_period vs paired crash_start/end decisions
- 3 month-precision terugval decisions
- whether to keep all 13 bedrijfsarts consults or filter
- whether to override any titles with shorter labels

## What happens after you share the Sheet

1. Pipeline fetches the CSV.
2. A dispatch script reads `action_to_take`:
   - `accept` → adds to `triage_events.csv` with source-tag
     `pwc_dossier_2022-2024` using suggested category and dossier title
     (or `user_label_override` if filled).
   - `skip` → recorded in audit trail, not added.
   - `change_category:X` → adds with overridden category.
   - `change_label:X` → adds with overridden label.
3. `merge_calendar_triage.py` re-runs (picks up the new triage events).
4. `build_timeline.py` re-renders.
5. Methodology updated to record dossier as second authoritative
   objective source.

## Why this matters

The dossier is the most authoritative source we have for the
reintegration period. It will materially:

- Fill the 16-day June 2023 crash (currently only 5/17 days as crash
  in `labels_crash_v2.csv`) into the annotations layer.
- Fill the 7-day January 2024 uitval (currently 0/7 as crash).
- Add 13 missing bedrijfsarts visits to the medical layer.
- Establish the 24-month wachttijd umbrella as durable context.

After this round lands, the §3a brainfog / spierpijn hypothesis test
will have hard objective crash boundaries to validate against, not
just the subjective `labels_crash_v2.csv` set.
