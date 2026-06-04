# Step 6 (v1.6.1 — explicit defer marker): Calendar-bound episodes (Shape B)

**Status:** Deferred — v1.6.1 follow-up to v1.6.
**Trigger to graduate:** v1.6 soak data shows the user is frequently linking multiple events to a single episode — typically ≥ 5 events linked to the same episode over a sustained period (e.g. every Tuesday's yoga event → "Yoga met Anna" episode). That repetition signals "this episode IS a calendar series; the per-event linking is friction we can remove."
**Why deferred:** Shape A (event-side linking via `calendar_events.linked_episode_id`) is sufficient until the linking patterns are observed. Shape B opens design questions that weren't in the v1.6 design conversations:
- What happens to a bound episode when the user excludes the bound series?
- What happens when the calendar event is moved or cancelled?
- Is promotion to bound-episode a manual user action, or automatic when N events of the same recurrence link to the same episode?

Settling those questions on soak data is much better than settling them on speculation.

---

## What this step would deliver

The reserved `episodes.calendar_binding` column (currently locked to `null` by the domain validator, with a comment pointing here per v1.6 step-0 AC0.36-AC0.38) gets unlocked + a defined shape + a UX for "promote a recurring series to an episode that auto-tracks it."

## Proposed shape

### Data

- `episodes.calendar_binding` shape: `{ provider: 'google' | 'microsoft'; connection_id: string; recurrence_id: string } | null`
- Validator unlocked: accepts the shape above OR `null`. Rejects malformed objects.
- New domain function `isCalendarBoundEpisode(episode: Episode): boolean` for type guards in components.

### UX

- In the per-event sheet (from v1.6 step-1), a NEW action for recurring events: `[Maak episode van deze serie]`. Tap → opens a small form to seed the episode name + category (mentaal / fysiek / interventie / etc), then creates an `episodes` row with `calendar_binding = { ... }` filled.
- A bound episode renders differently in the Periodes section: date fields are read-only with a small label `gekoppeld aan Google Calendar serie`. Edit form disables `start_date` / `end_date` (derived from the recurrence).
- A bound episode's start_date = first occurrence pulled, end_date = last occurrence pulled (or `null` if the recurrence is open-ended / Google's "no end date").
- If the user excludes the bound series (sluit-uit op een van de occurrences), the bound episode is NOT auto-archived. The exclusion only affects context-rendering; the episode is a separate user artifact. Cleanup is a separate action.
- An `[Ontkoppel van kalender]` action on the bound episode form removes the binding (sets `calendar_binding = null`); the episode then becomes a regular user-edited episode.

### Sync behavior

- Sync orchestrator (`src/lib/sync/calendar-sync.ts`) gains a step AFTER event upsert that updates bound episodes:
  - For each connection's bound episodes, find the matching `recurrence_id` events in the connection, compute new start/end dates, PATCH the episode if the dates have changed.

### Lifecycle edge cases

- **Recurrence cancelled in calendar** → next sync sees no events for that recurrence_id; bound episode's `end_date` stays at the last-known occurrence date. The episode is NOT auto-archived (preserves the user's history).
- **Recurrence moved** → bound episode's date fields update on next sync.
- **Connection disconnected** → bound episodes' `calendar_binding` is set to NULL (or status flagged "binding broken"; design decision at trigger time). Episodes survive disconnect.

### Schema impact

- Domain validator update.
- New Directus collection constraint: CHECK on `episodes.calendar_binding` shape (via app-layer validation, since Postgres can't enforce JSON shape via CHECK easily).
- No data migration (all existing rows have `calendar_binding = null` per the v1.5+ gate).

## Out of scope at trigger time

- Automatic promotion based on linking patterns (e.g. "this recurrence has 5 events all linked to the same episode → auto-promote"). v1.6.1 makes promotion a deliberate user action. Auto-promotion is a v1.6.2+ candidate if soak shows demand.
- Editing the bound recurrence from inside the app (we read-only the calendar; that's the v1.6 line).
- Multi-connection bound episodes (an episode bound to one Google calendar + one Outlook calendar simultaneously).

## Acceptance criteria, technical constraints, and test plan

To be filled in at trigger time. The structure mirrors v1.6 step-1; the surface is smaller (no new routes — extends existing ones) but the lifecycle edge cases need their own enumerated tests.

## Comment to update at trigger time

When this step graduates:

- `src/lib/domain/episode.ts` line 14-15 comment: `v1.6.1 → shipped in vX.Y` + remove the validator gate.
- `src/lib/api/episodes.ts` lines 105-108: same.
- v1.6 step-0 README: mark AC0.36-AC0.38 as "obsolete; calendar-bound episodes shipped in vX.Y".

## Done

Not applicable until graduated.
