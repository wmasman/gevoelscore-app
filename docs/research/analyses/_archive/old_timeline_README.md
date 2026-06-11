# Research timeline

**Purpose**: a single five-year visualisation of all the context we have for
this n-of-1 Long COVID investigation, so future research has rich context
to plot signals against.

**Spans**: 2021-08-16 (first Garmin day) → 2026-06-05 (latest data).

**Triage methodology**: see [`methodology.md`](methodology.md) for the
labelling conventions, 1-3 load scale definition, and decision rules
used when triaging calendar events and day-entry notes into
`annotations.yaml`.

**What's layered on the timeline** (top → bottom):

1. **Episode bands** — multi-day events from
   [`data/annotations.yaml`](data/annotations.yaml) (user-curated) + crashes
   + dips (from research labels).
2. **Point markers** — single-day events from `data/annotations.yaml`.
3. **gevoelscore line** — daily score 1-10, from
   [`labels_crash_v2.csv`](../garmin/hypotheses/crash_v2-definition/labels_crash_v2.csv).
4. **Resting HR** — from
   [`daily_uds.csv`](../garmin/activity-labels/output/daily_uds.csv).
5. **Sleep stress mean** — from
   [`sleep_stress_nightly.csv`](../garmin/scripts/sleep_stress_extract/sleep_stress_nightly.csv).
6. **Effective exertion** — from
   [`activity_features_daily.csv`](../garmin/activity-labels/output/activity_features_daily.csv).
7. **Stress spike duration** — from
   [`daily_max_spike.csv`](../garmin/hypotheses/H02b-stress-spikes/daily_max_spike.csv).

Era boundaries marked as vertical lines:
- 2022-05-06 — Long COVID diagnosis
- 2022-09-03 — gevoelscore tracking start
- 2023-12-31 — train / validate split boundary

## How to update

1. Add a one-day event or multi-day span to
   [`data/annotations.yaml`](data/annotations.yaml). See
   [`data/annotations.example.yaml`](data/annotations.example.yaml) for the
   schema.

2. Re-run:
   ```
   python docs/research/timeline/scripts/build_timeline.py
   ```

3. Output: [`output/timeline.png`](output/timeline.png) (overwritten on each
   run).

## Why a research artefact (not an app feature yet)

Phase 1 is **research-side only**: we want to see whether layering this
context surfaces useful patterns before deciding whether to ship a similar
view in the app. The app already has the data scaffolding ([`episodes`
collection](../../../directus/scripts/add-episodes.mjs) + the shipped
[`timeline-episode-overlay`](../../features/timeline-episode-overlay/)
feature) — re-using it for the Phase 2 in-app version will be cheap if the
research timeline proves its worth.

## Source-of-truth boundaries

- **gevoelscores + crash/dip labels** live in the research pipeline. The
  timeline script reads them but does not write back.
- **Annotations** (one-day markers, multi-day spans) live in
  [`data/annotations.yaml`](data/annotations.yaml) — this file is the
  source of truth for user-curated context. When Phase 2 imports this into
  Directus's `episodes` collection, the YAML will become the migration
  source.
- **Garmin daily features** live in the activity-labels research output.
  The timeline reads them; the eventual in-app version will read from
  `garmin_daily` (Directus collection, currently a placeholder).

## Data-quality caveats

- **Calendar coverage starts 2022-06-17 in Directus**. The Google Calendar
  sync did not backfill earlier events. Pre-coverage context for 2022
  (Long COVID onset year) is therefore thin — only the events the user
  manually pinned (via `📌` titles) and the events the user explicitly
  reconstructed for `annotations.yaml`.

- **Mixed work/private agenda in early period**. For roughly 2022 and
  early 2023, the user used the work agenda for both work and private
  events. The data sources we read (private calendar) therefore
  under-represent private context for that period. Newer years
  (~mid-2023 onwards) separated work from private and have richer
  private-event coverage. Any analysis that compares "event density"
  across years should account for this — apparent growth in events
  over time partly reflects improved agenda hygiene, not actual life
  intensity change.

- **Anecdotal correlations are not findings**. Inspecting the timeline
  alongside research-derived crash labels can surface tempting
  patterns (e.g. clusters of high-intensity events preceding crashes).
  These are descriptive observations, not statistical findings — no
  pre-registered null sample, no significance test. Treat them as
  context for the user's own sense-making, not as evidence to fold
  back into the synthesis docs or playbook.

- **Backfill recency bias on load annotations**. The triaged
  `keep_yn` + per-event `cognitive / physical / emotional` load
  values were applied in 2026-06 by the user looking back at events
  from 2022 through 2026. **Older events have less and less accurate
  load information** — the user remembers the recent year (2026) in
  vivid detail and applied loads on many events, while 2022 has
  almost no loads filled in (because memory of that period is less
  fine-grained). This explains the apparent growth in
  `high_intensity` event counts over time: it partly reflects
  recall fidelity, not actual change in life intensity. Any
  longitudinal analysis on load counts should account for this
  backfill bias.

- **Some interventies are not in the calendar**. CPAP-interventie
  (jan-mar 2025), Mirjam-relatiecoaching umbrella (2024), and a few
  others were added from user memory rather than from calendar
  events. Start/end dates for these may be globally accurate but
  not date-precise. The annotation notes flag these with "TODO:
  precieze datum bevestigen" where applicable.
