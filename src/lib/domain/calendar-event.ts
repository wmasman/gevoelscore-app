// Smart-default include/exclude rules for calendar events at pull time.
// Calendar-binding feature, v1.6.
//
// Three rules, priority order:
//   1. series-exclusion override (highest priority) — if the event's
//      recurrence is in the user's exclusion set, exclude.
//   2. declined RSVP → exclude.
//   3. all-day event → include.
//   4. recurring event (not series-excluded, not declined, not all-day)
//      → include with a UI badge.
//   5. else → include.
//
// NO keyword stoplist. Title content is ignored. Reason: keyword lists
// are paternalistic and the user-correction of 2026-06-03 ("blocks-to-do-
// work matter") established that we can't pre-guess what's noise.
//
// Pure function: same input → same output. No I/O, no clock, no
// randomness.

import type { CalendarEvent } from '@/lib/integrations/calendar-provider';

export type DefaultIncludedReason =
  | 'all_day'
  | 'recurring'
  | 'declined'
  | 'series_excluded'
  | 'default';

export type DefaultIncludedResult = {
  included: boolean;
  reason: DefaultIncludedReason;
};

export function computeDefaultIncluded(
  event: CalendarEvent,
  seriesExclusions: Set<string>,
): DefaultIncludedResult {
  // Rule 1: series-exclusion takes priority over everything else.
  // If the user has excluded this whole recurrence, defer to that
  // even if the event would otherwise be all-day or declined.
  if (event.recurrenceId !== null && seriesExclusions.has(event.recurrenceId)) {
    return { included: false, reason: 'series_excluded' };
  }

  // Rule 2: declined RSVP. The user explicitly said they didn't go.
  if (event.declined) {
    return { included: false, reason: 'declined' };
  }

  // Rule 3: all-day events are almost always context-worthy
  // (holidays, vacations, conferences, off-days).
  if (event.allDay) {
    return { included: true, reason: 'all_day' };
  }

  // Rule 4: recurring events are included by default. The UI shows a
  // recurrence badge so excluding the series is one tap away.
  if (event.recurrenceId !== null) {
    return { included: true, reason: 'recurring' };
  }

  // Rule 5: default — one-off non-declined event. Include.
  return { included: true, reason: 'default' };
}
