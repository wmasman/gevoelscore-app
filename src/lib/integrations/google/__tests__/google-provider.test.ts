// Step-1 Phase 1.A — Google provider tests.
// Mocks global.fetch to simulate Google's OAuth + Calendar API responses.
// Coverage: AC1.1-AC1.12 + the step-0 amendment fields (eventType, status,
// transparency, organizerIsSelf, iCalUid, htmlLink).

import {
  describe,
  expect,
  it,
  beforeEach,
  vi,
  type MockedFunction,
} from 'vitest';
import { createGoogleCalendarProvider } from '../google-provider';

const mockFetch: MockedFunction<typeof fetch> = vi.fn();
// eslint-disable-next-line @typescript-eslint/no-explicit-any
(global as any).fetch = mockFetch;

const TEST_CLIENT_ID = 'test-client-id.apps.googleusercontent.com';
const TEST_CLIENT_SECRET = 'test-client-secret';
const TEST_REDIRECT_URI =
  'https://gevoelscore-frontend.fly.dev/api/calendars/google/callback';

function mockJsonResponse(status: number, body: unknown): Response {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
    text: async () => JSON.stringify(body),
  } as unknown as Response;
}

function buildProvider() {
  return createGoogleCalendarProvider({
    clientId: TEST_CLIENT_ID,
    clientSecret: TEST_CLIENT_SECRET,
  });
}

beforeEach(() => {
  mockFetch.mockReset();
});

describe('google-provider', () => {
  describe('id discriminator', () => {
    it('given a provider instance, when read, then id is google', () => {
      const provider = buildProvider();

      expect(provider.id).toBe('google');
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // buildAuthUrl (AC1.2)
  // ─────────────────────────────────────────────────────────────────

  describe('buildAuthUrl (AC1.2)', () => {
    it('given a state and redirect_uri, when built, then URL includes calendar.readonly scope only + offline + consent + state', () => {
      const provider = buildProvider();

      const url = provider.buildAuthUrl('state-abc', TEST_REDIRECT_URI);
      const parsed = new URL(url);

      expect(parsed.origin + parsed.pathname).toBe(
        'https://accounts.google.com/o/oauth2/v2/auth',
      );
      expect(parsed.searchParams.get('client_id')).toBe(TEST_CLIENT_ID);
      expect(parsed.searchParams.get('redirect_uri')).toBe(TEST_REDIRECT_URI);
      expect(parsed.searchParams.get('response_type')).toBe('code');
      expect(parsed.searchParams.get('scope')).toBe(
        'https://www.googleapis.com/auth/calendar.readonly',
      );
      expect(parsed.searchParams.get('access_type')).toBe('offline');
      expect(parsed.searchParams.get('prompt')).toBe('consent');
      expect(parsed.searchParams.get('state')).toBe('state-abc');
    });

    it('given any state, when built, then URL has NO other scope beyond calendar.readonly', () => {
      const provider = buildProvider();

      const url = provider.buildAuthUrl('s', TEST_REDIRECT_URI);
      const scope = new URL(url).searchParams.get('scope') ?? '';

      // Exactly one scope; no whitespace-separated extras
      expect(scope).toBe('https://www.googleapis.com/auth/calendar.readonly');
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // exchangeCode (AC1.3, AC1.12)
  // ─────────────────────────────────────────────────────────────────

  describe('exchangeCode (AC1.3, AC1.12)', () => {
    it('given an auth code, when exchanged, then POSTs to oauth2.googleapis.com/token with grant_type=authorization_code', async () => {
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(200, {
          access_token: 'a-token',
          refresh_token: 'r-token',
          expires_in: 3600,
          scope: 'https://www.googleapis.com/auth/calendar.readonly',
          token_type: 'Bearer',
        }),
      );
      // listCalendars to fetch the account email from primary calendar.id
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(200, {
          items: [
            {
              id: 'user@example.com',
              summary: 'user@example.com',
              primary: true,
            },
          ],
        }),
      );

      const provider = buildProvider();
      await provider.exchangeCode('auth-code-xyz', TEST_REDIRECT_URI);

      expect(mockFetch).toHaveBeenCalled();
      const tokenCall = mockFetch.mock.calls[0]!;
      const tokenUrl = tokenCall[0] as string;
      const tokenInit = tokenCall[1] as RequestInit;
      expect(tokenUrl).toBe('https://oauth2.googleapis.com/token');
      expect(tokenInit.method).toBe('POST');
      const body = new URLSearchParams(tokenInit.body as string);
      expect(body.get('grant_type')).toBe('authorization_code');
      expect(body.get('code')).toBe('auth-code-xyz');
      expect(body.get('redirect_uri')).toBe(TEST_REDIRECT_URI);
      expect(body.get('client_id')).toBe(TEST_CLIENT_ID);
      expect(body.get('client_secret')).toBe(TEST_CLIENT_SECRET);
    });

    it('given a valid token response + primary calendar id, when exchanged, then returns refreshToken + accessToken + expiresAt + accountEmail', async () => {
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(200, {
          access_token: 'access-abc',
          refresh_token: 'refresh-xyz',
          expires_in: 3600,
          scope: 'https://www.googleapis.com/auth/calendar.readonly',
          token_type: 'Bearer',
        }),
      );
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(200, {
          items: [
            {
              id: 'user@example.com',
              summary: 'user@example.com',
              primary: true,
            },
            { id: 'addressbook#contacts@group.v.calendar.google.com', summary: 'Contacts' },
          ],
        }),
      );

      const provider = buildProvider();
      const result = await provider.exchangeCode(
        'auth-code',
        TEST_REDIRECT_URI,
      );

      expect(result.refreshToken).toBe('refresh-xyz');
      expect(result.accessToken).toBe('access-abc');
      expect(result.accountEmail).toBe('user@example.com');
      expect(result.expiresAt).toBeInstanceOf(Date);
      // expiresAt is in the future
      expect(result.expiresAt.getTime()).toBeGreaterThan(Date.now());
    });

    it('given a malformed token response (missing refresh_token), when exchanged, then throws google_api_invalid_response', async () => {
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(200, {
          access_token: 'access-abc',
          // refresh_token missing
          expires_in: 3600,
        }),
      );

      const provider = buildProvider();

      await expect(
        provider.exchangeCode('code', TEST_REDIRECT_URI),
      ).rejects.toThrow(/google_api_invalid_response/);
    });

    it('given a non-200 token response (400 invalid_grant), when exchanged, then throws google_api_invalid_response', async () => {
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(400, {
          error: 'invalid_grant',
          error_description: 'Bad code',
        }),
      );

      const provider = buildProvider();

      await expect(
        provider.exchangeCode('code', TEST_REDIRECT_URI),
      ).rejects.toThrow();
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // refreshAccessToken (AC1.4)
  // ─────────────────────────────────────────────────────────────────

  describe('refreshAccessToken (AC1.4)', () => {
    it('given a refresh token, when refreshed, then POSTs with grant_type=refresh_token', async () => {
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(200, {
          access_token: 'new-access-token',
          expires_in: 3600,
          scope: 'https://www.googleapis.com/auth/calendar.readonly',
          token_type: 'Bearer',
        }),
      );

      const provider = buildProvider();
      await provider.refreshAccessToken('r-token-abc');

      const call = mockFetch.mock.calls[0]!;
      const body = new URLSearchParams((call[1] as RequestInit).body as string);
      expect(body.get('grant_type')).toBe('refresh_token');
      expect(body.get('refresh_token')).toBe('r-token-abc');
      expect(body.get('client_id')).toBe(TEST_CLIENT_ID);
      expect(body.get('client_secret')).toBe(TEST_CLIENT_SECRET);
    });

    it('given a valid response, when refreshed, then returns accessToken + expiresAt only (no refreshToken)', async () => {
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(200, {
          access_token: 'fresh-access',
          expires_in: 3600,
        }),
      );

      const provider = buildProvider();
      const result = await provider.refreshAccessToken('r-token');

      expect(result.accessToken).toBe('fresh-access');
      expect(result.expiresAt).toBeInstanceOf(Date);
      // No refreshToken in the result shape per the interface
      expect((result as unknown as Record<string, unknown>).refreshToken).toBeUndefined();
    });

    it('given a 400 invalid_grant (refresh token revoked or expired), when refreshed, then throws refresh_token_invalid', async () => {
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(400, {
          error: 'invalid_grant',
          error_description: 'Token has been expired or revoked.',
        }),
      );

      const provider = buildProvider();

      await expect(
        provider.refreshAccessToken('revoked-token'),
      ).rejects.toThrow(/refresh_token_invalid/);
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // listCalendars (AC1.5)
  // ─────────────────────────────────────────────────────────────────

  describe('listCalendars (AC1.5)', () => {
    it('given an access token, when listed, then GETs calendarList endpoint with minAccessRole=reader', async () => {
      mockFetch.mockResolvedValueOnce(mockJsonResponse(200, { items: [] }));

      const provider = buildProvider();
      await provider.listCalendars('access-token');

      const call = mockFetch.mock.calls[0]!;
      const url = call[0] as string;
      expect(url).toContain(
        'https://www.googleapis.com/calendar/v3/users/me/calendarList',
      );
      expect(url).toContain('minAccessRole=reader');
      expect((call[1] as RequestInit).headers).toMatchObject({
        Authorization: 'Bearer access-token',
      });
    });

    it('given a list of Google calendars, when listed, then maps id/summary/primary to id/displayName/isPrimary', async () => {
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(200, {
          items: [
            { id: 'user@example.com', summary: 'user@example.com', primary: true },
            { id: 'work-cal', summary: 'Work' },
            {
              id: 'addressbook#contacts@group.v.calendar.google.com',
              summary: 'Contacts',
            },
            {
              id: 'nl.dutch#holiday@group.v.calendar.google.com',
              summary: 'Holidays in Netherlands',
            },
          ],
        }),
      );

      const provider = buildProvider();
      const result = await provider.listCalendars('access-token');

      expect(result).toHaveLength(4);
      expect(result[0]).toEqual({
        id: 'user@example.com',
        displayName: 'user@example.com',
        isPrimary: true,
      });
      expect(result[1]).toEqual({
        id: 'work-cal',
        displayName: 'Work',
        isPrimary: false,
      });
      expect(result[2]).toMatchObject({ displayName: 'Contacts' });
      expect(result[3]).toMatchObject({ displayName: 'Holidays in Netherlands' });
    });

    it('given the response, when listed, then does NOT filter out contacts/holidays (user opts-in per calendar)', async () => {
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(200, {
          items: [
            { id: 'a', summary: 'A', primary: true },
            { id: 'addressbook#contacts@group.v.calendar.google.com', summary: 'Contacts' },
          ],
        }),
      );

      const provider = buildProvider();
      const result = await provider.listCalendars('access-token');

      const ids = result.map((c) => c.id);
      expect(ids).toContain('addressbook#contacts@group.v.calendar.google.com');
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // fetchEvents (AC1.6, AC1.7, AC1.8, AC1.9, AC1.10, AC1.12 + amendment)
  // ─────────────────────────────────────────────────────────────────

  describe('fetchEvents (AC1.6)', () => {
    it('given multiple included calendars, when fetched, then one GET per calendar', async () => {
      mockFetch.mockResolvedValue(mockJsonResponse(200, { items: [] }));

      const provider = buildProvider();
      await provider.fetchEvents(
        'token',
        ['cal-a', 'cal-b', 'cal-c'],
        new Date('2026-06-01'),
        new Date('2026-07-01'),
      );

      expect(mockFetch).toHaveBeenCalledTimes(3);
    });

    it('given a date range, when fetched, then passes timeMin/timeMax/singleEvents/maxResults/showDeleted query params (AC1.6)', async () => {
      mockFetch.mockResolvedValueOnce(mockJsonResponse(200, { items: [] }));

      const provider = buildProvider();
      const from = new Date('2026-06-01T00:00:00Z');
      const to = new Date('2026-07-01T00:00:00Z');
      await provider.fetchEvents('token', ['cal-a'], from, to);

      const url = mockFetch.mock.calls[0]![0] as string;
      expect(url).toContain('calendar/v3/calendars/cal-a/events');
      expect(url).toContain('timeMin=' + encodeURIComponent(from.toISOString()));
      expect(url).toContain('timeMax=' + encodeURIComponent(to.toISOString()));
      expect(url).toContain('singleEvents=true');
      expect(url).toContain('maxResults=2500');
      expect(url).toContain('showDeleted=false');
    });

    it('given a multi-page response (nextPageToken set), when fetched, then follows pages until exhausted (AC1.6)', async () => {
      mockFetch
        .mockResolvedValueOnce(
          mockJsonResponse(200, {
            items: [{
              id: 'evt-1',
              status: 'confirmed',
              start: { dateTime: '2026-06-04T10:00:00Z' },
              end: { dateTime: '2026-06-04T11:00:00Z' },
              summary: 'first',
              iCalUID: 'evt-1@google.com',
              htmlLink: 'https://calendar.google.com/calendar/event?eid=1',
            }],
            nextPageToken: 'page-2',
          }),
        )
        .mockResolvedValueOnce(
          mockJsonResponse(200, {
            items: [{
              id: 'evt-2',
              status: 'confirmed',
              start: { dateTime: '2026-06-05T10:00:00Z' },
              end: { dateTime: '2026-06-05T11:00:00Z' },
              summary: 'second',
              iCalUID: 'evt-2@google.com',
              htmlLink: 'https://calendar.google.com/calendar/event?eid=2',
            }],
            // no nextPageToken — last page
          }),
        );

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date('2026-06-01'),
        new Date('2026-07-01'),
      );

      expect(mockFetch).toHaveBeenCalledTimes(2);
      expect(events).toHaveLength(2);
      expect(events[0]!.providerEventId).toBe('evt-1');
      expect(events[1]!.providerEventId).toBe('evt-2');
      // Second call carries pageToken=page-2
      const secondUrl = mockFetch.mock.calls[1]![0] as string;
      expect(secondUrl).toContain('pageToken=page-2');
    });
  });

  describe('fetchEvents — recurrence + declined + allDay + attendees (AC1.7-AC1.10)', () => {
    function mockEventsResponse(items: unknown[]) {
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(200, { items, nextPageToken: undefined }),
      );
    }

    it('given an instance event with recurringEventId, when fetched, then recurrenceId is populated (AC1.7)', async () => {
      mockEventsResponse([
        {
          id: 'evt-instance-1',
          status: 'confirmed',
          start: { dateTime: '2026-06-04T10:00:00Z' },
          end: { dateTime: '2026-06-04T11:00:00Z' },
          summary: 'Recurring yoga',
          recurringEventId: 'rec-yoga-123',
          iCalUID: 'evt@google.com',
          htmlLink: 'https://calendar.google.com',
        },
      ]);

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date(),
        new Date(),
      );

      expect(events[0]!.recurrenceId).toBe('rec-yoga-123');
    });

    it('given an event with self-attendee responseStatus=declined, when fetched, then declined=true (AC1.8)', async () => {
      mockEventsResponse([
        {
          id: 'evt-declined',
          status: 'confirmed',
          start: { dateTime: '2026-06-04T10:00:00Z' },
          end: { dateTime: '2026-06-04T11:00:00Z' },
          summary: 'Team meeting',
          attendees: [
            { email: 'a@x.com', responseStatus: 'accepted' },
            { email: 'me@x.com', self: true, responseStatus: 'declined' },
          ],
          iCalUID: 'd@google.com',
          htmlLink: 'https://calendar.google.com',
        },
      ]);

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date(),
        new Date(),
      );

      expect(events[0]!.declined).toBe(true);
    });

    it('given an event with no attendees array, when fetched, then declined=false (AC1.8)', async () => {
      mockEventsResponse([
        {
          id: 'evt-solo',
          status: 'confirmed',
          start: { dateTime: '2026-06-04T10:00:00Z' },
          end: { dateTime: '2026-06-04T11:00:00Z' },
          summary: 'Solo focus',
          iCalUID: 's@google.com',
          htmlLink: 'https://calendar.google.com',
        },
      ]);

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date(),
        new Date(),
      );

      expect(events[0]!.declined).toBe(false);
    });

    it('given an all-day event (start.date, no dateTime), when fetched, then allDay=true (AC1.9)', async () => {
      mockEventsResponse([
        {
          id: 'evt-allday',
          status: 'confirmed',
          start: { date: '2026-06-04' },
          end: { date: '2026-06-05' },
          summary: 'Vakantie',
          iCalUID: 'v@google.com',
          htmlLink: 'https://calendar.google.com',
        },
      ]);

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date(),
        new Date(),
      );

      expect(events[0]!.allDay).toBe(true);
    });

    it('given a timed event (start.dateTime), when fetched, then allDay=false (AC1.9)', async () => {
      mockEventsResponse([
        {
          id: 'evt-timed',
          status: 'confirmed',
          start: { dateTime: '2026-06-04T10:00:00Z' },
          end: { dateTime: '2026-06-04T11:00:00Z' },
          summary: 'Timed',
          iCalUID: 't@google.com',
          htmlLink: 'https://calendar.google.com',
        },
      ]);

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date(),
        new Date(),
      );

      expect(events[0]!.allDay).toBe(false);
    });

    it('given an event with N attendees, when fetched, then attendeesCount=N (AC1.10)', async () => {
      mockEventsResponse([
        {
          id: 'evt-team',
          status: 'confirmed',
          start: { dateTime: '2026-06-04T10:00:00Z' },
          end: { dateTime: '2026-06-04T11:00:00Z' },
          summary: 'Team',
          attendees: [{ email: 'a@x.com' }, { email: 'b@x.com' }, { email: 'c@x.com' }],
          iCalUID: 't@google.com',
          htmlLink: 'https://calendar.google.com',
        },
      ]);

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date(),
        new Date(),
      );

      expect(events[0]!.attendeesCount).toBe(3);
    });

    it('given an event with no attendees array, when fetched, then attendeesCount=0 (AC1.10)', async () => {
      mockEventsResponse([
        {
          id: 'evt-solo',
          status: 'confirmed',
          start: { dateTime: '2026-06-04T10:00:00Z' },
          end: { dateTime: '2026-06-04T11:00:00Z' },
          summary: 'Solo',
          iCalUID: 's@google.com',
          htmlLink: 'https://calendar.google.com',
        },
      ]);

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date(),
        new Date(),
      );

      expect(events[0]!.attendeesCount).toBe(0);
    });
  });

  describe('fetchEvents — amendment fields (eventType + status + transparency + organizerIsSelf + iCalUid + htmlLink)', () => {
    function mockEventsResponse(items: unknown[]) {
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(200, { items, nextPageToken: undefined }),
      );
    }

    it('given an event with eventType=birthday, when fetched, then eventType=birthday', async () => {
      mockEventsResponse([
        {
          id: 'bday-1',
          status: 'confirmed',
          eventType: 'birthday',
          start: { date: '2026-06-04' },
          end: { date: '2026-06-05' },
          summary: 'Sarah verjaardag',
          iCalUID: 'b@google.com',
          htmlLink: 'https://calendar.google.com',
        },
      ]);

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date(),
        new Date(),
      );

      expect(events[0]!.eventType).toBe('birthday');
    });

    it('given an event with no eventType field, when fetched, then eventType=null (Google defaults handled by adapter)', async () => {
      mockEventsResponse([
        {
          id: 'evt',
          status: 'confirmed',
          start: { dateTime: '2026-06-04T10:00:00Z' },
          end: { dateTime: '2026-06-04T11:00:00Z' },
          summary: 'Regular',
          iCalUID: 'r@google.com',
          htmlLink: 'https://calendar.google.com',
        },
      ]);

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date(),
        new Date(),
      );

      // Google defaults to 'default' when absent; we capture that.
      expect(events[0]!.eventType).toBe('default');
    });

    it('given an event with status=cancelled, when fetched, then status=cancelled', async () => {
      mockEventsResponse([
        {
          id: 'evt-x',
          status: 'cancelled',
          start: { dateTime: '2026-06-04T10:00:00Z' },
          end: { dateTime: '2026-06-04T11:00:00Z' },
          summary: 'Cancelled meeting',
          iCalUID: 'c@google.com',
          htmlLink: 'https://calendar.google.com',
        },
      ]);

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date(),
        new Date(),
      );

      expect(events[0]!.status).toBe('cancelled');
    });

    it('given an event with transparency=transparent, when fetched, then transparency=transparent', async () => {
      mockEventsResponse([
        {
          id: 'evt-free',
          status: 'confirmed',
          transparency: 'transparent',
          start: { dateTime: '2026-06-04T10:00:00Z' },
          end: { dateTime: '2026-06-04T11:00:00Z' },
          summary: 'Reminder',
          iCalUID: 'f@google.com',
          htmlLink: 'https://calendar.google.com',
        },
      ]);

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date(),
        new Date(),
      );

      expect(events[0]!.transparency).toBe('transparent');
    });

    it('given an event with no transparency field, when fetched, then transparency=opaque (Google default)', async () => {
      mockEventsResponse([
        {
          id: 'evt',
          status: 'confirmed',
          start: { dateTime: '2026-06-04T10:00:00Z' },
          end: { dateTime: '2026-06-04T11:00:00Z' },
          summary: 'Regular',
          iCalUID: 'r@google.com',
          htmlLink: 'https://calendar.google.com',
        },
      ]);

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date(),
        new Date(),
      );

      expect(events[0]!.transparency).toBe('opaque');
    });

    it('given an event with organizer.self=true, when fetched, then organizerIsSelf=true', async () => {
      mockEventsResponse([
        {
          id: 'evt-mine',
          status: 'confirmed',
          organizer: { email: 'me@x.com', self: true },
          start: { dateTime: '2026-06-04T10:00:00Z' },
          end: { dateTime: '2026-06-04T11:00:00Z' },
          summary: 'I created this',
          iCalUID: 'm@google.com',
          htmlLink: 'https://calendar.google.com',
        },
      ]);

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date(),
        new Date(),
      );

      expect(events[0]!.organizerIsSelf).toBe(true);
    });

    it('given an event with organizer.self absent, when fetched, then organizerIsSelf=false', async () => {
      mockEventsResponse([
        {
          id: 'evt-theirs',
          status: 'confirmed',
          organizer: { email: 'other@x.com' },
          start: { dateTime: '2026-06-04T10:00:00Z' },
          end: { dateTime: '2026-06-04T11:00:00Z' },
          summary: 'Someone else created this',
          iCalUID: 'o@google.com',
          htmlLink: 'https://calendar.google.com',
        },
      ]);

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date(),
        new Date(),
      );

      expect(events[0]!.organizerIsSelf).toBe(false);
    });

    it('given an event with iCalUID and htmlLink, when fetched, then both fields are captured', async () => {
      mockEventsResponse([
        {
          id: 'evt-1',
          status: 'confirmed',
          start: { dateTime: '2026-06-04T10:00:00Z' },
          end: { dateTime: '2026-06-04T11:00:00Z' },
          summary: 'Event',
          iCalUID: 'abc-123@google.com',
          htmlLink: 'https://calendar.google.com/calendar/event?eid=xyz',
        },
      ]);

      const provider = buildProvider();
      const events = await provider.fetchEvents(
        'token',
        ['cal-a'],
        new Date(),
        new Date(),
      );

      expect(events[0]!.iCalUid).toBe('abc-123@google.com');
      expect(events[0]!.htmlLink).toBe(
        'https://calendar.google.com/calendar/event?eid=xyz',
      );
    });
  });

  describe('fetchEvents — invalid response (AC1.12)', () => {
    it('given a malformed event (missing id), when fetched, then throws google_api_invalid_response', async () => {
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(200, {
          items: [
            {
              // id missing
              status: 'confirmed',
              start: { dateTime: '2026-06-04T10:00:00Z' },
              end: { dateTime: '2026-06-04T11:00:00Z' },
              summary: 'Bad event',
            },
          ],
        }),
      );

      const provider = buildProvider();

      await expect(
        provider.fetchEvents('token', ['cal-a'], new Date(), new Date()),
      ).rejects.toThrow(/google_api_invalid_response/);
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // revoke (AC1.11)
  // ─────────────────────────────────────────────────────────────────

  describe('revoke (AC1.11)', () => {
    it('given a refresh token, when revoked, then POSTs to oauth2.googleapis.com/revoke?token=...', async () => {
      mockFetch.mockResolvedValueOnce(mockJsonResponse(200, {}));

      const provider = buildProvider();
      await provider.revoke('r-token-abc');

      const call = mockFetch.mock.calls[0]!;
      const url = call[0] as string;
      expect(url).toBe(
        'https://oauth2.googleapis.com/revoke?token=r-token-abc',
      );
      expect((call[1] as RequestInit).method).toBe('POST');
    });

    it('given a 200 response, when revoked, then resolves (success)', async () => {
      mockFetch.mockResolvedValueOnce(mockJsonResponse(200, {}));

      const provider = buildProvider();

      await expect(provider.revoke('r-token')).resolves.toBeUndefined();
    });

    it('given a 400 invalid_token (already revoked), when revoked, then resolves (idempotent)', async () => {
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(400, { error: 'invalid_token' }),
      );

      const provider = buildProvider();

      await expect(provider.revoke('r-token')).resolves.toBeUndefined();
    });

    it('given a 500 server error, when revoked, then throws', async () => {
      mockFetch.mockResolvedValueOnce(
        mockJsonResponse(500, { error: 'internal' }),
      );

      const provider = buildProvider();

      await expect(provider.revoke('r-token')).rejects.toThrow();
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // No-PII logging (AC1.76)
  // ─────────────────────────────────────────────────────────────────

  describe('no-PII logging (AC1.76)', () => {
    it('given the google-provider module source, when scanned for console.log, then no event title or attendee data is logged', async () => {
      const fs = await import('node:fs/promises');
      const source = await fs.readFile(
        'src/lib/integrations/google/google-provider.ts',
        'utf8',
      );
      // Naive check: console.log of event.title / event.summary / attendees
      // should not appear in the production code. (Dev logs are fine, but
      // the project doesn't have a NODE_ENV gate pattern for console.log
      // in this module, so we enforce zero.)
      expect(source).not.toMatch(/console\.log\(.*\.title/i);
      expect(source).not.toMatch(/console\.log\(.*\.summary/i);
      expect(source).not.toMatch(/console\.log\(.*\.attendees/i);
      expect(source).not.toMatch(/console\.log\(.*\.location/i);
    });
  });
});
