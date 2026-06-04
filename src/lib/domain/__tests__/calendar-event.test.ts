// Step-0 AC0.4-AC0.7: smart-default rules at pull time.
// Three rules in priority order: series-exclusion override > declined > all-day > recurring > default.
// No keyword stoplist; title content is ignored.

import { describe, expect, it } from 'vitest';
import { computeDefaultIncluded } from '../calendar-event';
import type { CalendarEvent } from '@/lib/integrations/calendar-provider';

function baseEvent(overrides: Partial<CalendarEvent> = {}): CalendarEvent {
  return {
    providerEventId: 'evt-default',
    sourceCalendarId: 'cal-primary@gmail.com',
    recurrenceId: null,
    startAt: new Date('2026-06-04T10:00:00Z'),
    endAt: new Date('2026-06-04T11:00:00Z'),
    allDay: false,
    title: 'Default event',
    location: null,
    attendeesCount: 0,
    declined: false,
    eventType: 'default',
    status: 'confirmed',
    transparency: 'opaque',
    organizerIsSelf: false,
    iCalUid: null,
    htmlLink: null,
    ...overrides,
  };
}

describe('calendar-event', () => {
  describe('computeDefaultIncluded — three smart-default rules', () => {
    it('given a series-excluded recurring event, when defaulted, then excluded with reason=series_excluded (AC0.4)', () => {
      const event = baseEvent({ recurrenceId: 'rec-yoga' });

      const result = computeDefaultIncluded(event, new Set(['rec-yoga']));

      expect(result).toEqual({ included: false, reason: 'series_excluded' });
    });

    it('given a declined RSVP event, when defaulted, then excluded with reason=declined (AC0.4)', () => {
      const event = baseEvent({ declined: true });

      const result = computeDefaultIncluded(event, new Set());

      expect(result).toEqual({ included: false, reason: 'declined' });
    });

    it('given an all-day event, when defaulted, then included with reason=all_day (AC0.4)', () => {
      const event = baseEvent({ allDay: true });

      const result = computeDefaultIncluded(event, new Set());

      expect(result).toEqual({ included: true, reason: 'all_day' });
    });

    it('given a recurring event (not series-excluded, not declined, not all-day), when defaulted, then included with reason=recurring (AC0.4)', () => {
      const event = baseEvent({ recurrenceId: 'rec-coaching' });

      const result = computeDefaultIncluded(event, new Set());

      expect(result).toEqual({ included: true, reason: 'recurring' });
    });

    it('given a one-off non-declined event, when defaulted, then included with reason=default (AC0.4)', () => {
      const event = baseEvent();

      const result = computeDefaultIncluded(event, new Set());

      expect(result).toEqual({ included: true, reason: 'default' });
    });

    it('given an all-day event whose recurrence is series-excluded, when defaulted, then series-exclusion takes priority (AC0.4)', () => {
      const event = baseEvent({ allDay: true, recurrenceId: 'rec-holiday' });

      const result = computeDefaultIncluded(event, new Set(['rec-holiday']));

      expect(result).toEqual({ included: false, reason: 'series_excluded' });
    });

    it('given a declined recurring event whose series is excluded, when defaulted, then series-exclusion takes priority over declined (AC0.4)', () => {
      const event = baseEvent({
        declined: true,
        recurrenceId: 'rec-deep-meeting',
      });

      const result = computeDefaultIncluded(
        event,
        new Set(['rec-deep-meeting']),
      );

      expect(result).toEqual({ included: false, reason: 'series_excluded' });
    });

    it('given an event with a keyword-like title (Standup), when defaulted, then title content is ignored (AC0.6)', () => {
      const event = baseEvent({ title: 'Standup with team' });

      const result = computeDefaultIncluded(event, new Set());

      expect(result).toEqual({ included: true, reason: 'default' });
    });

    it('given the same input twice, when defaulted, then yields the same output (purity — AC0.7)', () => {
      const event = baseEvent({ recurrenceId: 'rec-foo' });
      const exclusions = new Set(['rec-foo']);

      const a = computeDefaultIncluded(event, exclusions);
      const b = computeDefaultIncluded(event, exclusions);

      expect(a).toEqual(b);
    });
  });
});
