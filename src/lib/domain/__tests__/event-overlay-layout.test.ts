// Step-3 Phase 3.A — buildEventOverlayLayout (AC3.1-3.7).
//
// Pure data function: events + range + tz → { markerDays, spans }. Tests
// cover the timezone-correct day-enumeration, range clipping, dedup,
// and the included-as-context filter. Performance test is informational
// (a benchmark, not a strict assertion).

import { describe, expect, it } from 'vitest';
import {
  buildEventOverlayLayout,
  type EventOverlayLayout,
} from '../event-overlay-layout';
import type { DirectusCalendarEventRow } from '@/lib/api/calendars';

const TZ = 'Europe/Amsterdam';

function evt(
  overrides: Partial<DirectusCalendarEventRow> = {},
): DirectusCalendarEventRow {
  return {
    id: 'evt-default',
    connection_id: 'conn-1',
    provider: 'google',
    provider_event_id: 'pg-default',
    source_calendar_id: 'cal-primary@gmail.com',
    recurrence_id: null,
    start_at: '2026-06-05T10:00:00Z',
    end_at: '2026-06-05T11:00:00Z',
    all_day: false,
    title: 'Fysio',
    location: null,
    attendees_count: 0,
    declined: false,
    event_type: 'default',
    status: 'confirmed',
    transparency: 'opaque',
    organizer_is_self: false,
    ical_uid: null,
    html_link: null,
    linked_tag_id: null,
    linked_episode_id: null,
    included_as_context: true,
    user_decision: 'auto',
    created_at: '2026-06-05T10:00:00Z',
    updated_at: '2026-06-05T10:00:00Z',
    ...overrides,
  };
}

describe('buildEventOverlayLayout (AC3.1-3.7)', () => {
  // Use a wide range that covers all fixture dates so range-clipping
  // isn't an accidental confound in tests 1-6, 8-11.
  const RANGE_START = new Date('2026-05-01T00:00:00Z');
  const RANGE_END = new Date('2026-07-01T00:00:00Z');

  it('test 90 (AC3.1, AC3.15): empty events → empty layout', () => {
    const result = buildEventOverlayLayout([], RANGE_START, RANGE_END, TZ);

    expect(result).toEqual<EventOverlayLayout>({
      markerDays: new Set(),
      spans: [],
    });
  });

  it('test 91 (AC3.4, AC3.5): single-day event → markerDays has that date, spans empty', () => {
    // 2026-06-05 12:00-13:00 Europe/Amsterdam (= 10:00-11:00 UTC summer)
    const result = buildEventOverlayLayout(
      [evt({ start_at: '2026-06-05T10:00:00Z', end_at: '2026-06-05T11:00:00Z' })],
      RANGE_START,
      RANGE_END,
      TZ,
    );

    expect([...result.markerDays]).toEqual(['2026-06-05']);
    expect(result.spans).toEqual([]);
  });

  it('test 92 (AC3.4, AC3.5): multi-day event (2 days) → markerDays has both dates, spans has 1', () => {
    const result = buildEventOverlayLayout(
      [
        evt({
          start_at: '2026-06-05T08:00:00Z', // 10:00 local
          end_at: '2026-06-06T08:00:00Z',   // 10:00 local next day
          recurrence_id: null,
        }),
      ],
      RANGE_START,
      RANGE_END,
      TZ,
    );

    expect([...result.markerDays].sort()).toEqual(['2026-06-05', '2026-06-06']);
    expect(result.spans).toEqual([
      { recurrenceId: null, startDate: '2026-06-05', endDate: '2026-06-06' },
    ]);
  });

  it('test 93 (AC3.5): multi-day event (7 days) → markerDays has all 7 dates, spans has 1', () => {
    const result = buildEventOverlayLayout(
      [
        evt({
          start_at: '2026-06-01T07:00:00Z', // 09:00 local
          end_at: '2026-06-07T15:00:00Z',   // 17:00 local
        }),
      ],
      RANGE_START,
      RANGE_END,
      TZ,
    );

    expect([...result.markerDays].sort()).toEqual([
      '2026-06-01',
      '2026-06-02',
      '2026-06-03',
      '2026-06-04',
      '2026-06-05',
      '2026-06-06',
      '2026-06-07',
    ]);
    expect(result.spans).toHaveLength(1);
    expect(result.spans[0]!.startDate).toBe('2026-06-01');
    expect(result.spans[0]!.endDate).toBe('2026-06-07');
  });

  it('test 94 (AC3.4): multiple single-day events on the same day → markerDays has 1 entry (deduped)', () => {
    const result = buildEventOverlayLayout(
      [
        evt({ id: 'a', start_at: '2026-06-05T08:00:00Z', end_at: '2026-06-05T09:00:00Z' }),
        evt({ id: 'b', start_at: '2026-06-05T13:00:00Z', end_at: '2026-06-05T14:00:00Z' }),
        evt({ id: 'c', start_at: '2026-06-05T18:00:00Z', end_at: '2026-06-05T19:00:00Z' }),
      ],
      RANGE_START,
      RANGE_END,
      TZ,
    );

    expect([...result.markerDays]).toEqual(['2026-06-05']);
    expect(result.spans).toEqual([]);
  });

  it('test 95 (AC3.3): excluded event (included_as_context=false) → not in markerDays or spans', () => {
    const result = buildEventOverlayLayout(
      [
        evt({
          id: 'in',
          start_at: '2026-06-05T08:00:00Z',
          end_at: '2026-06-05T09:00:00Z',
          included_as_context: true,
        }),
        evt({
          id: 'out',
          start_at: '2026-06-06T08:00:00Z',
          end_at: '2026-06-08T09:00:00Z',
          included_as_context: false,
        }),
      ],
      RANGE_START,
      RANGE_END,
      TZ,
    );

    expect([...result.markerDays]).toEqual(['2026-06-05']);
    expect(result.spans).toEqual([]);
  });

  it('test 96 (AC3.4, range clipping): multi-day event partially outside range → only in-range dates + clipped span', () => {
    // Event spans 2026-05-29 → 2026-06-05 (8 days)
    // Range: 2026-06-01T00:00Z → 2026-06-04T00:00Z (3-day window in local)
    // Wait: range bounds are TIMESTAMPS not local-dates, so the cutoff
    // depends on tz. 2026-06-04T00:00Z = 2026-06-04 02:00 local.
    // Last in-range LOCAL date = 2026-06-04 (the chunk between 00:00-02:00
    // local on the 4th IS in range). Use a tz-aware range to avoid the
    // off-by-2-hours confusion.
    const result = buildEventOverlayLayout(
      [
        evt({
          start_at: '2026-05-29T08:00:00Z',
          end_at: '2026-06-05T08:00:00Z',
        }),
      ],
      new Date('2026-06-01T00:00:00+02:00'), // 2026-06-01 00:00 local
      new Date('2026-06-04T00:00:00+02:00'), // 2026-06-04 00:00 local (exclusive)
      TZ,
    );

    expect([...result.markerDays].sort()).toEqual([
      '2026-06-01',
      '2026-06-02',
      '2026-06-03',
    ]);
    expect(result.spans).toHaveLength(1);
    expect(result.spans[0]!.startDate).toBe('2026-06-01');
    expect(result.spans[0]!.endDate).toBe('2026-06-03');
  });

  it('test 97 (AC3.5): event spanning UTC midnight but not local midnight → single day in user tz', () => {
    // Event: 2026-06-05 23:00 UTC → 2026-06-06 00:30 UTC.
    // In Amsterdam summer (UTC+2): 2026-06-06 01:00 → 2026-06-06 02:30 local.
    // Single local day (06-06), no span.
    const result = buildEventOverlayLayout(
      [
        evt({
          start_at: '2026-06-05T23:00:00Z',
          end_at: '2026-06-06T00:30:00Z',
        }),
      ],
      RANGE_START,
      RANGE_END,
      TZ,
    );

    expect([...result.markerDays]).toEqual(['2026-06-06']);
    expect(result.spans).toEqual([]);
  });

  it('test 98 (AC3.4): event ending at 23:59 local Tuesday → markerDays has Tuesday only', () => {
    // 2026-06-02 is a Tuesday. 21:00-21:59 UTC = 23:00-23:59 local (summer).
    const result = buildEventOverlayLayout(
      [
        evt({
          start_at: '2026-06-02T20:00:00Z', // 22:00 local
          end_at: '2026-06-02T21:59:00Z',   // 23:59 local
        }),
      ],
      RANGE_START,
      RANGE_END,
      TZ,
    );

    expect([...result.markerDays]).toEqual(['2026-06-02']);
    expect(result.spans).toEqual([]);
  });

  it('test 99 (AC3.4): event from Tuesday 23:00 to Wednesday 01:00 local → markerDays has Tuesday + Wednesday', () => {
    // 2026-06-02 Tuesday 23:00 local = 21:00 UTC (summer).
    // 2026-06-03 Wednesday 01:00 local = 23:00 UTC (Tue).
    const result = buildEventOverlayLayout(
      [
        evt({
          start_at: '2026-06-02T21:00:00Z',
          end_at: '2026-06-02T23:00:00Z',
        }),
      ],
      RANGE_START,
      RANGE_END,
      TZ,
    );

    expect([...result.markerDays].sort()).toEqual(['2026-06-02', '2026-06-03']);
    expect(result.spans).toEqual([
      { recurrenceId: null, startDate: '2026-06-02', endDate: '2026-06-03' },
    ]);
  });

  it('test 100 (AC3.6): spans carry recurrence_id correctly', () => {
    const result = buildEventOverlayLayout(
      [
        evt({
          start_at: '2026-06-05T08:00:00Z',
          end_at: '2026-06-06T08:00:00Z',
          recurrence_id: 'rec-yoga',
        }),
      ],
      RANGE_START,
      RANGE_END,
      TZ,
    );

    expect(result.spans).toEqual([
      { recurrenceId: 'rec-yoga', startDate: '2026-06-05', endDate: '2026-06-06' },
    ]);
  });

  it('test 101 (AC3.7, performance): 200 events in 90-day window resolves in < 50ms (informational)', () => {
    // Spec says < 5ms; assert < 50ms to be lenient against CI noise and
    // still catch O(N^2)-shaped regressions (which would blow past 50ms
    // for these inputs).
    const events: DirectusCalendarEventRow[] = [];
    for (let i = 0; i < 200; i++) {
      const dayOffset = i % 90;
      const startStr = new Date(2026, 5, 1 + dayOffset, 10).toISOString();
      const endStr = new Date(2026, 5, 1 + dayOffset, 11).toISOString();
      events.push(
        evt({
          id: `e${i}`,
          start_at: startStr,
          end_at: endStr,
        }),
      );
    }

    const start = performance.now();
    buildEventOverlayLayout(
      events,
      new Date('2026-06-01T00:00:00Z'),
      new Date('2026-09-01T00:00:00Z'),
      TZ,
    );
    const elapsedMs = performance.now() - start;

    expect(elapsedMs).toBeLessThan(50);
  });
});
