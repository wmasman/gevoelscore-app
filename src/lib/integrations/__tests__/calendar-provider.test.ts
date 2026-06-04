// Step-0 AC0.1-AC0.3: locks the CalendarProvider interface shape +
// canonical CalendarEvent shape. If either changes, this test must be
// updated explicitly so the change is deliberate.

import { describe, expect, it } from 'vitest';
import type {
  CalendarEvent,
  CalendarProvider,
} from '../calendar-provider';

describe('calendar-provider', () => {
  describe('CalendarProvider interface shape (AC0.1)', () => {
    it('given a mock implementation, when typed as CalendarProvider, then has all 6 required methods + id discriminator', () => {
      const mockProvider: CalendarProvider = {
        id: 'google',
        buildAuthUrl: () => 'https://example.test/auth',
        exchangeCode: async () => ({
          refreshToken: 't',
          accessToken: 'a',
          expiresAt: new Date(0),
          accountEmail: 'e@example.test',
        }),
        refreshAccessToken: async () => ({
          accessToken: 'a',
          expiresAt: new Date(0),
        }),
        listCalendars: async () => [],
        fetchEvents: async () => [],
        revoke: async () => {},
      };

      expect(mockProvider.id).toBe('google');
      expect(typeof mockProvider.buildAuthUrl).toBe('function');
      expect(typeof mockProvider.exchangeCode).toBe('function');
      expect(typeof mockProvider.refreshAccessToken).toBe('function');
      expect(typeof mockProvider.listCalendars).toBe('function');
      expect(typeof mockProvider.fetchEvents).toBe('function');
      expect(typeof mockProvider.revoke).toBe('function');
    });
  });

  describe('CalendarEvent canonical shape (AC0.2)', () => {
    it('given a CalendarEvent object, when its keys are inspected, then has exactly the 15 canonical fields', () => {
      const event: CalendarEvent = {
        providerEventId: 'evt-1',
        recurrenceId: null,
        startAt: new Date('2026-06-04T10:00:00Z'),
        endAt: new Date('2026-06-04T11:00:00Z'),
        allDay: false,
        title: 'Fysiotherapie',
        location: 'Praktijk',
        attendeesCount: 1,
        declined: false,
        eventType: 'default',
        status: 'confirmed',
        transparency: 'opaque',
        organizerIsSelf: true,
        iCalUid: 'abc-123@google.com',
        htmlLink: 'https://calendar.google.com/calendar/event?eid=xxx',
      };

      const keys = Object.keys(event).sort();

      expect(keys).toEqual([
        'allDay',
        'attendeesCount',
        'declined',
        'endAt',
        'eventType',
        'htmlLink',
        'iCalUid',
        'location',
        'organizerIsSelf',
        'providerEventId',
        'recurrenceId',
        'startAt',
        'status',
        'title',
        'transparency',
      ]);
    });

    it('given a CalendarEvent with null-able fields nulled, when typed, then the optional fields accept null', () => {
      const event: CalendarEvent = {
        providerEventId: 'evt-2',
        recurrenceId: null,
        startAt: new Date('2026-06-04T10:00:00Z'),
        endAt: new Date('2026-06-04T11:00:00Z'),
        allDay: false,
        title: 'Untyped event',
        location: null,
        attendeesCount: 0,
        declined: false,
        eventType: null,
        status: 'confirmed',
        transparency: 'opaque',
        organizerIsSelf: false,
        iCalUid: null,
        htmlLink: null,
      };

      expect(event.eventType).toBeNull();
      expect(event.iCalUid).toBeNull();
      expect(event.htmlLink).toBeNull();
    });

    it('given a CalendarEvent status, when typed, then accepts only confirmed | tentative | cancelled', () => {
      // Compile-time check: a status of 'foo' would be a TS error.
      // Runtime check: the three valid values are accepted.
      const confirmed: CalendarEvent['status'] = 'confirmed';
      const tentative: CalendarEvent['status'] = 'tentative';
      const cancelled: CalendarEvent['status'] = 'cancelled';

      expect([confirmed, tentative, cancelled]).toEqual([
        'confirmed',
        'tentative',
        'cancelled',
      ]);
    });
  });
});
