# How to triage `reintegration_gaps_review.csv`

37 gaps surfaced by the first PwC cross-validation pass. Same workflow as
the per-year intensity triage rounds:

1. Upload [`data/reintegration_gaps_review.csv`](reintegration_gaps_review.csv)
   to a new Google Sheet.
2. For each row, fill in the `action_to_take` column with one of the
   vocabulary terms below.
3. Optionally use the `notes` column for clarification.
4. Share the Sheet link back with me; the pipeline picks it up.

## Quick stats

| gap type | count | what it is |
|---|---:|---|
| `work_heavy_no_load` | 21 | day with 4+ PwC work-hours, no cog_load in per_day_intensity |
| `doctor_visit_missing` | 12 | bedrijfsarts / huisarts / casemanager / ergotherapeut visit not in annotations |
| `illness_stretch` | 4 | 3+ consecutive sick days in PwC log |

## The `action_to_take` vocabulary

Use exactly these strings (case-insensitive). Empty / blank = "no action".

| action_to_take | what happens |
|---|---|
| `add_cog_load:1` | adds cog=1 (light) to per_day_intensity.csv for this date |
| `add_cog_load:2` | adds cog=2 (moderate) |
| `add_cog_load:3` | adds cog=3 (heavy) |
| `add_event` | adds a new event to triage_events.csv with category=`medical` (for doctor visits) |
| `mark_dip` | adds the worst day of the stretch to sub_threshold_dips.csv |
| `skip` | explicit "no action needed" — useful for vacation days or routine check-ins |

You can also add a brief `notes` value explaining your reasoning
(especially useful for `skip` so future-you knows why).

## How to decide per gap type

### `work_heavy_no_load` (21 rows)

These are days where you worked 4+ hours at PwC but the
per_day_intensity database has no cog_load. Most likely:

- **Add cog_load** if the day was genuinely cognitively heavy. Use the
  `pwc_note` column for context (what did you do that day?).
  - 4 hours of focused project work, design, or client meetings → `add_cog_load:2`
  - 5+ hours with multiple meetings + new content → `add_cog_load:3`
  - 4 hours of mostly admin / emails / reading → `add_cog_load:1`
- **Skip** if the day was actually:
  - vacation but counted hours wrongly,
  - a "naar amsterdam" day already captured as a PwC umbrella event,
  - or a low-effort day despite the hours.

The `score` column shows the gevoelscore that day if available — useful
calibration. A 4-hour day with score=4 is more cog-heavy than a 4-hour
day with score=7.

### `doctor_visit_missing` (12 rows)

These are bedrijfsarts / huisarts / casemanager / ergotherapeut /
jobcoach visits in the PwC log not yet in annotations.yaml.

- **Add event** for visits that materially shaped that day or signal
  a treatment phase boundary:
  - bedrijfsarts (3 visits): `add_event` — these are key reintegration
    moments
  - casemanager visits during the reintegration plan negotiation:
    `add_event`
  - ergotherapeut (2 visits): `add_event` if it was a substantive
    session
- **Skip** for brief phone-only check-ins or visits whose only purpose
  was admin (e.g. signing forms).

### `illness_stretch` (4 rows)

These are 3+ day sick periods from the PwC log. Reassuring news:
**3 of the 4 already 100% overlap** with existing dip/crash labels, so
they're likely already in the database. The one with partial overlap:

- **2023-11-14 → 11-17** (4 dgn, 3 of 4 dgn already marked) — the
  4th day is the gap. Confirm: was this the same PEM-stretch (then
  `mark_dip` on the missing day), or did you start to recover that day
  (then `skip`).

## What happens after you fill the sheet

1. You share the Sheet link.
2. I fetch the CSV.
3. A small dispatch script reads `action_to_take` per row:
   - `add_cog_load:N` → upserts the row into `per_day_intensity.csv`
     with source `pwc_cross_validation_2026-06-11`.
   - `add_event` → upserts into `triage_events.csv` with category
     `medical` and source `pwc_cross_validation_2026-06-11`.
   - `mark_dip` → upserts into `sub_threshold_dips.csv`.
   - `skip` → recorded as intentionally-not-actioned (kept in the
     review file for audit trail).
4. Mergers re-run. Timeline re-renders. Heatstripes refresh with the
   new cog_loads visible in 2022-09 → 2024-02.

## What this is not

- **Not a re-triage.** The existing per_day_intensity values are not
  touched. This pass only **fills in cog_loads where there was no
  value**.
- **Not authoritative.** The PwC log is one objective source. A
  contradicting gevoelscore or note may override an `add_cog_load`
  suggestion. Your judgement wins; the action_to_take column is yours
  to set as you see fit.

## Estimated effort

~30 min for 37 rows. Most `work_heavy_no_load` rows resolve in seconds
once you read the `pwc_note` column. The `doctor_visit_missing` rows
take a bit longer per-row (decide if the visit shaped the day). The
illness stretches are quick — most are already covered.
