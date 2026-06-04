// Singleton accessor for the Google Calendar provider. Routes import this
// instead of calling createGoogleCalendarProvider directly so tests can
// vi.mock the singleton.
//
// Reads GOOGLE_CLIENT_ID + GOOGLE_CLIENT_SECRET from Fly secrets / .env.local
// at first call. Throws if either is missing — the route handler surfaces
// this as a 500 with no PII (per AC1.78).

import type { CalendarProvider } from '@/lib/integrations/calendar-provider';
import { createGoogleCalendarProvider } from './google-provider';

let cached: CalendarProvider | null = null;

export function getGoogleProvider(): CalendarProvider {
  if (cached) return cached;
  const clientId = process.env.GOOGLE_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_CLIENT_SECRET;
  if (!clientId || !clientSecret) {
    throw new Error(
      'GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set as Fly secrets',
    );
  }
  cached = createGoogleCalendarProvider({ clientId, clientSecret });
  return cached;
}

// Test helper: reset the cached singleton between tests.
export function resetGoogleProviderCache(): void {
  cached = null;
}
