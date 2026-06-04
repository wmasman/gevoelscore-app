// Google Calendar adapter implementing the CalendarProvider interface.
// Calendar-binding feature, step-1 Phase 1.A.
//
// Network calls are direct via global fetch. Manual narrowing of Google's
// JSON responses (mirrors the validateEpisode pattern in src/lib/domain/).
// Throws 'google_api_invalid_response' or 'refresh_token_invalid' for
// specific failure modes the caller (sync orchestrator + OAuth routes)
// needs to distinguish.
//
// NO console.log of titles / locations / attendees / tokens. Counts and
// IDs only, and even those don't leak to chat-visible logs because there
// are no console.log calls in this module at all.

import type {
  CalendarEvent,
  CalendarProvider,
} from '@/lib/integrations/calendar-provider';

export type GoogleProviderOptions = {
  clientId: string;
  clientSecret: string;
};

const GOOGLE_AUTH_BASE = 'https://accounts.google.com/o/oauth2/v2/auth';
const GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token';
const GOOGLE_REVOKE_URL = 'https://oauth2.googleapis.com/revoke';
const GOOGLE_CALENDAR_LIST_URL =
  'https://www.googleapis.com/calendar/v3/users/me/calendarList';
const GOOGLE_EVENTS_URL_BASE =
  'https://www.googleapis.com/calendar/v3/calendars';
const CALENDAR_READONLY_SCOPE =
  'https://www.googleapis.com/auth/calendar.readonly';

// ─────────────────────────────────────────────────────────────────
// Manual narrowing helpers. Mirrors the domain-validator convention
// (typeof + key checks). Throws explicit errors so the caller can
// distinguish "Google sent us garbage" from other failures.
// ─────────────────────────────────────────────────────────────────

function isRecord(x: unknown): x is Record<string, unknown> {
  return typeof x === 'object' && x !== null && !Array.isArray(x);
}

function invalidResponse(detail: string): never {
  throw new Error(`google_api_invalid_response: ${detail}`);
}

type GoogleTokenResponse = {
  access_token: string;
  refresh_token: string;
  expires_in: number;
  scope?: string;
  token_type?: string;
};

function parseExchangeResponse(raw: unknown): GoogleTokenResponse {
  if (!isRecord(raw)) invalidResponse('token response not an object');
  if (typeof raw.access_token !== 'string')
    invalidResponse('token.access_token missing');
  if (typeof raw.refresh_token !== 'string')
    invalidResponse('token.refresh_token missing');
  if (typeof raw.expires_in !== 'number')
    invalidResponse('token.expires_in missing');
  return {
    access_token: raw.access_token,
    refresh_token: raw.refresh_token,
    expires_in: raw.expires_in,
    scope: typeof raw.scope === 'string' ? raw.scope : undefined,
    token_type: typeof raw.token_type === 'string' ? raw.token_type : undefined,
  };
}

type GoogleRefreshResponse = {
  access_token: string;
  expires_in: number;
};

function parseRefreshResponse(raw: unknown): GoogleRefreshResponse {
  if (!isRecord(raw)) invalidResponse('refresh response not an object');
  if (typeof raw.access_token !== 'string')
    invalidResponse('refresh.access_token missing');
  if (typeof raw.expires_in !== 'number')
    invalidResponse('refresh.expires_in missing');
  return {
    access_token: raw.access_token,
    expires_in: raw.expires_in,
  };
}

type GoogleCalendarListEntry = {
  id: string;
  summary: string;
  primary?: boolean;
};

function parseCalendarListResponse(raw: unknown): GoogleCalendarListEntry[] {
  if (!isRecord(raw)) invalidResponse('calendarList response not an object');
  const items = raw.items;
  if (!Array.isArray(items))
    invalidResponse('calendarList.items not an array');
  return items.map((item, idx) => {
    if (!isRecord(item))
      invalidResponse(`calendarList.items[${idx}] not an object`);
    if (typeof item.id !== 'string')
      invalidResponse(`calendarList.items[${idx}].id missing`);
    if (typeof item.summary !== 'string')
      invalidResponse(`calendarList.items[${idx}].summary missing`);
    return {
      id: item.id,
      summary: item.summary,
      primary: item.primary === true,
    };
  });
}

type GoogleEventTimeRef = { date?: string; dateTime?: string };

type GoogleEvent = {
  id: string;
  status: string;
  eventType?: string;
  transparency?: string;
  start: GoogleEventTimeRef;
  end: GoogleEventTimeRef;
  summary?: string;
  location?: string;
  recurringEventId?: string;
  attendees?: Array<{ self?: boolean; responseStatus?: string }>;
  organizer?: { self?: boolean };
  iCalUID: string;
  htmlLink: string;
};

function parseEventTimeRef(raw: unknown, label: string): GoogleEventTimeRef {
  if (!isRecord(raw)) invalidResponse(`${label} not an object`);
  const result: GoogleEventTimeRef = {};
  if (typeof raw.date === 'string') result.date = raw.date;
  if (typeof raw.dateTime === 'string') result.dateTime = raw.dateTime;
  if (!result.date && !result.dateTime)
    invalidResponse(`${label} has neither date nor dateTime`);
  return result;
}

function parseGoogleEvent(raw: unknown, idx: number): GoogleEvent {
  if (!isRecord(raw)) invalidResponse(`events[${idx}] not an object`);
  if (typeof raw.id !== 'string')
    invalidResponse(`events[${idx}].id missing`);
  if (typeof raw.status !== 'string')
    invalidResponse(`events[${idx}].status missing`);
  if (typeof raw.iCalUID !== 'string')
    invalidResponse(`events[${idx}].iCalUID missing`);
  if (typeof raw.htmlLink !== 'string')
    invalidResponse(`events[${idx}].htmlLink missing`);

  const start = parseEventTimeRef(raw.start, `events[${idx}].start`);
  const end = parseEventTimeRef(raw.end, `events[${idx}].end`);

  const event: GoogleEvent = {
    id: raw.id,
    status: raw.status,
    start,
    end,
    iCalUID: raw.iCalUID,
    htmlLink: raw.htmlLink,
  };
  if (typeof raw.eventType === 'string') event.eventType = raw.eventType;
  if (typeof raw.transparency === 'string') event.transparency = raw.transparency;
  if (typeof raw.summary === 'string') event.summary = raw.summary;
  if (typeof raw.location === 'string') event.location = raw.location;
  if (typeof raw.recurringEventId === 'string')
    event.recurringEventId = raw.recurringEventId;
  if (Array.isArray(raw.attendees)) {
    event.attendees = raw.attendees.map((a) => {
      if (!isRecord(a)) return {};
      return {
        self: a.self === true,
        responseStatus:
          typeof a.responseStatus === 'string' ? a.responseStatus : undefined,
      };
    });
  }
  if (isRecord(raw.organizer)) {
    event.organizer = { self: raw.organizer.self === true };
  }
  return event;
}

type GoogleEventsListResponse = {
  items: GoogleEvent[];
  nextPageToken?: string;
};

function parseEventsListResponse(raw: unknown): GoogleEventsListResponse {
  if (!isRecord(raw)) invalidResponse('events response not an object');
  if (!Array.isArray(raw.items)) invalidResponse('events.items not an array');
  return {
    items: raw.items.map(parseGoogleEvent),
    nextPageToken:
      typeof raw.nextPageToken === 'string' ? raw.nextPageToken : undefined,
  };
}

function mapToCanonical(g: GoogleEvent): CalendarEvent {
  const isAllDay = g.start.date !== undefined && g.start.dateTime === undefined;
  const startAt = new Date(g.start.dateTime ?? `${g.start.date}T00:00:00Z`);
  const endAt = new Date(g.end.dateTime ?? `${g.end.date}T00:00:00Z`);

  const attendees = g.attendees ?? [];
  const declined = attendees.some(
    (a) => a.self === true && a.responseStatus === 'declined',
  );

  return {
    providerEventId: g.id,
    recurrenceId: g.recurringEventId ?? null,
    startAt,
    endAt,
    allDay: isAllDay,
    title: g.summary ?? '',
    location: g.location ?? null,
    attendeesCount: attendees.length,
    declined,
    eventType: g.eventType ?? 'default',
    status:
      g.status === 'confirmed' || g.status === 'tentative' || g.status === 'cancelled'
        ? g.status
        : 'confirmed',
    transparency: g.transparency === 'transparent' ? 'transparent' : 'opaque',
    organizerIsSelf: g.organizer?.self === true,
    iCalUid: g.iCalUID,
    htmlLink: g.htmlLink,
  };
}

// ─────────────────────────────────────────────────────────────────
// Provider factory
// ─────────────────────────────────────────────────────────────────

export function createGoogleCalendarProvider(
  opts: GoogleProviderOptions,
): CalendarProvider {
  const { clientId, clientSecret } = opts;

  async function postForm(
    url: string,
    body: Record<string, string>,
  ): Promise<{ status: number; data: unknown; text: string }> {
    const formBody = new URLSearchParams(body).toString();
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formBody,
    });
    const text = await response.text();
    let data: unknown = null;
    try {
      data = text ? JSON.parse(text) : null;
    } catch {
      // ignore — caller handles non-JSON
    }
    return { status: response.status, data, text };
  }

  async function getJson(
    url: string,
    accessToken: string,
  ): Promise<{ status: number; data: unknown; text: string }> {
    const response = await fetch(url, {
      method: 'GET',
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    const text = await response.text();
    let data: unknown = null;
    try {
      data = text ? JSON.parse(text) : null;
    } catch {
      // ignore
    }
    return { status: response.status, data, text };
  }

  return {
    id: 'google',

    buildAuthUrl(state: string, redirectUri: string): string {
      const params = new URLSearchParams({
        client_id: clientId,
        redirect_uri: redirectUri,
        response_type: 'code',
        scope: CALENDAR_READONLY_SCOPE,
        access_type: 'offline',
        prompt: 'consent',
        state,
      });
      return `${GOOGLE_AUTH_BASE}?${params.toString()}`;
    },

    async exchangeCode(code: string, redirectUri: string) {
      const { status, data } = await postForm(GOOGLE_TOKEN_URL, {
        grant_type: 'authorization_code',
        code,
        redirect_uri: redirectUri,
        client_id: clientId,
        client_secret: clientSecret,
      });
      if (status !== 200) {
        invalidResponse(`exchangeCode HTTP ${status}`);
      }
      const tokens = parseExchangeResponse(data);

      // Fetch the primary calendar to get the account email.
      const list = await this.listCalendars(tokens.access_token);
      const primary = list.find((c) => c.isPrimary);
      const accountEmail = primary?.id ?? list[0]?.id;
      if (!accountEmail) {
        invalidResponse('no calendars found after exchangeCode');
      }

      return {
        refreshToken: tokens.refresh_token,
        accessToken: tokens.access_token,
        expiresAt: new Date(Date.now() + tokens.expires_in * 1000),
        accountEmail,
      };
    },

    async refreshAccessToken(refreshToken: string) {
      const { status, data } = await postForm(GOOGLE_TOKEN_URL, {
        grant_type: 'refresh_token',
        refresh_token: refreshToken,
        client_id: clientId,
        client_secret: clientSecret,
      });
      if (status === 400) {
        // Google returns 400 invalid_grant when the refresh token is
        // revoked/expired. Caller (sync orchestrator) needs to surface
        // this as a connection.status='error' rather than a generic
        // failure.
        throw new Error('refresh_token_invalid');
      }
      if (status !== 200) {
        invalidResponse(`refreshAccessToken HTTP ${status}`);
      }
      const parsed = parseRefreshResponse(data);
      return {
        accessToken: parsed.access_token,
        expiresAt: new Date(Date.now() + parsed.expires_in * 1000),
      };
    },

    async listCalendars(accessToken: string) {
      const url = `${GOOGLE_CALENDAR_LIST_URL}?minAccessRole=reader`;
      const { status, data } = await getJson(url, accessToken);
      if (status !== 200) {
        invalidResponse(`listCalendars HTTP ${status}`);
      }
      const parsed = parseCalendarListResponse(data);
      return parsed.map((c) => ({
        id: c.id,
        displayName: c.summary,
        isPrimary: c.primary === true,
      }));
    },

    async fetchEvents(
      accessToken: string,
      includedCalendarIds: string[],
      from: Date,
      to: Date,
    ): Promise<CalendarEvent[]> {
      const all: CalendarEvent[] = [];
      for (const calId of includedCalendarIds) {
        let pageToken: string | undefined;
        do {
          const params = new URLSearchParams({
            timeMin: from.toISOString(),
            timeMax: to.toISOString(),
            singleEvents: 'true',
            maxResults: '2500',
            showDeleted: 'false',
          });
          if (pageToken) params.set('pageToken', pageToken);
          const url = `${GOOGLE_EVENTS_URL_BASE}/${encodeURIComponent(calId)}/events?${params.toString()}`;
          const { status, data } = await getJson(url, accessToken);
          if (status !== 200) {
            invalidResponse(`fetchEvents HTTP ${status}`);
          }
          const parsed = parseEventsListResponse(data);
          for (const item of parsed.items) {
            all.push(mapToCanonical(item));
          }
          pageToken = parsed.nextPageToken;
        } while (pageToken);
      }
      return all;
    },

    async revoke(refreshToken: string): Promise<void> {
      const url = `${GOOGLE_REVOKE_URL}?token=${encodeURIComponent(refreshToken)}`;
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });
      if (response.status === 200) return;
      // 400 invalid_token = already revoked. Treat as success.
      if (response.status === 400) {
        const text = await response.text();
        if (text.includes('invalid_token')) return;
        throw new Error(`revoke HTTP 400: ${text.slice(0, 100)}`);
      }
      throw new Error(`revoke HTTP ${response.status}`);
    },
  };
}
