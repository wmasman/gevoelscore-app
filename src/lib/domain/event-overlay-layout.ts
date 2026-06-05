// Step-3 Phase 3.A — pure derivation that turns event rows into the two
// visual primitives the timeline overlay renders (markerDays + spans).
//
// Server-side: the TimelineView's parent passes events + range + tz to
// this function and forwards the result to TimelineEventMarkers as a
// prop. Client component is presentational only (AC3.14).
//
// Day enumeration is timezone-aware: we walk yyyy-mm-dd strings in the
// user's timezone, not UTC. A 23:00 → 01:00 local event crosses one
// local midnight regardless of UTC offset; a 23:00 → 23:59 local event
// crosses none. The Intl.DateTimeFormat is hoisted out of the loop
// (caching it shaves ~5x off the per-event cost).
//
// AC3.1 - AC3.7.

import type { DirectusCalendarEventRow } from '@/lib/api/calendars';

export type EventOverlayLayout = {
  markerDays: Set<string>;
  spans: Array<{
    recurrenceId: string | null;
    startDate: string;
    endDate: string;
  }>;
};

function makeLocalDateFormatter(tz: string): Intl.DateTimeFormat {
  return new Intl.DateTimeFormat('sv-SE', {
    timeZone: tz,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
}

function nextDateStr(dateStr: string): string {
  const y = Number(dateStr.slice(0, 4));
  const m = Number(dateStr.slice(5, 7));
  const d = Number(dateStr.slice(8, 10));
  const next = new Date(Date.UTC(y, m - 1, d + 1));
  const yy = next.getUTCFullYear();
  const mm = String(next.getUTCMonth() + 1).padStart(2, '0');
  const dd = String(next.getUTCDate()).padStart(2, '0');
  return `${yy}-${mm}-${dd}`;
}

export function buildEventOverlayLayout(
  events: DirectusCalendarEventRow[],
  rangeStart: Date,
  rangeEnd: Date,
  userTimezone: string,
): EventOverlayLayout {
  const markerDays = new Set<string>();
  const spans: EventOverlayLayout['spans'] = [];
  const fmt = makeLocalDateFormatter(userTimezone);

  for (const evt of events) {
    if (!evt.included_as_context) continue;

    const start = new Date(evt.start_at);
    const end = new Date(evt.end_at);

    // Clip to range (rangeEnd exclusive). Skip events outside.
    const effectiveStart = start < rangeStart ? rangeStart : start;
    const effectiveEnd = end > rangeEnd ? rangeEnd : end;
    if (effectiveStart >= effectiveEnd) continue;

    // end is exclusive in overlap semantics, so the last covered local
    // day is whatever date (effectiveEnd - 1ms) falls on. Otherwise an
    // event ending at exactly local-midnight would count the next day.
    const startLocalDate = fmt.format(effectiveStart);
    const lastDayInclusive = fmt.format(
      new Date(effectiveEnd.getTime() - 1),
    );

    let cursor = startLocalDate;
    while (cursor <= lastDayInclusive) {
      markerDays.add(cursor);
      cursor = nextDateStr(cursor);
    }

    if (startLocalDate !== lastDayInclusive) {
      spans.push({
        recurrenceId: evt.recurrence_id,
        startDate: startLocalDate,
        endDate: lastDayInclusive,
      });
    }
  }

  return { markerDays, spans };
}
