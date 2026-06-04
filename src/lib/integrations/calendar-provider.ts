// CalendarProvider interface + canonical CalendarEvent type.
// Calendar-binding feature, v1.6. See docs/features/calendar-binding/.
//
// This module is TYPES ONLY — no implementation. The Google adapter
// lands in step-1 (src/lib/integrations/google/google-provider.ts).
// Future Outlook / Apple adapters slot in alongside without changing
// this file.

/**
 * Canonical CalendarEvent shape, provider-agnostic. Per-provider
 * adapters map their native event shape to this type.
 *
 * 15 fields, no provider-specific extensions. If a provider has an
 * additional concept (Google's etag, Microsoft's @odata.etag, etc),
 * it stays inside that provider's adapter and never reaches downstream
 * code.
 *
 * Field notes:
 *   - `eventType`: provider-classified event kind. Google's known
 *     values: 'default' | 'birthday' | 'focusTime' | 'outOfOffice' |
 *     'workingLocation' | 'fromGmail'. Null when the provider doesn't
 *     classify. v1.6 captures the field; smart-default rules don't
 *     branch on it yet (v1.6.x keyword rules + v2 learned rules will).
 *   - `status`: 'confirmed' (default) | 'tentative' | 'cancelled'.
 *     A future smart-default rule can exclude cancelled events.
 *   - `transparency`: 'opaque' (busy) | 'transparent' (free). 'free'
 *     events tend to be reminders / placeholders.
 *   - `organizerIsSelf`: true if the user organized the event. Higher
 *     context signal than invitations.
 *   - `iCalUid`: standard iCalendar UID (RFC 5545) for cross-provider
 *     dedup if multiple providers ever sync. Independent of
 *     providerEventId. Nullable; some providers don't expose it.
 *   - `htmlLink`: deep-link back to the provider's event UI. Used by
 *     the event detail sheet's "Open in Google Calendar" affordance.
 */
export type CalendarEvent = {
  providerEventId: string;
  recurrenceId: string | null;
  startAt: Date;
  endAt: Date;
  allDay: boolean;
  title: string;
  location: string | null;
  attendeesCount: number;
  declined: boolean;
  eventType: string | null;
  status: 'confirmed' | 'tentative' | 'cancelled';
  transparency: 'opaque' | 'transparent';
  organizerIsSelf: boolean;
  iCalUid: string | null;
  htmlLink: string | null;
  /**
   * The provider's calendar id this event came from (one Google account
   * can have many calendars). Populated by the adapter during fetchEvents
   * (which iterates per calendar). Used by the choose-calendars route
   * to delete events from a now-excluded calendar.
   */
  sourceCalendarId: string;
};

/**
 * Provider abstraction. 6 methods, one discriminator. Each provider
 * (Google v1.6, Outlook v2, Apple v2) implements this interface.
 *
 * Method contracts:
 *   - buildAuthUrl: returns the OAuth authorization URL given a signed
 *     state cookie value and the redirect URI. No network call; pure
 *     URL construction.
 *   - exchangeCode: exchanges an auth code for refresh + access tokens
 *     and the connection's account email. Network call to the provider's
 *     token endpoint.
 *   - refreshAccessToken: refreshes an access token from a stored
 *     refresh token. Network call.
 *   - listCalendars: lists the user's calendars (id + display name +
 *     primary flag). Network call. Used at connect time for the
 *     calendar-selection screen.
 *   - fetchEvents: fetches events in a bounded date window from the
 *     included calendar IDs. Network call(s); may paginate internally.
 *   - revoke: revokes the OAuth grant. Idempotent on the provider side
 *     (already-revoked is treated as success by adapters).
 */
export interface CalendarProvider {
  readonly id: 'google' | 'outlook' | 'apple';

  buildAuthUrl(state: string, redirectUri: string): string;

  exchangeCode(
    code: string,
    redirectUri: string,
  ): Promise<{
    refreshToken: string;
    accessToken: string;
    expiresAt: Date;
    accountEmail: string;
  }>;

  refreshAccessToken(refreshToken: string): Promise<{
    accessToken: string;
    expiresAt: Date;
  }>;

  listCalendars(
    accessToken: string,
  ): Promise<Array<{ id: string; displayName: string; isPrimary: boolean }>>;

  fetchEvents(
    accessToken: string,
    includedCalendarIds: string[],
    from: Date,
    to: Date,
  ): Promise<CalendarEvent[]>;

  revoke(refreshToken: string): Promise<void>;
}
