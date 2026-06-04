// GET /api/calendars/google/callback — completes the Google OAuth flow.
//
// Reads the `code` + `state` query params and the `cal_oauth_state` cookie,
// validates state match (CSRF protection), exchanges the code for tokens,
// fetches the primary calendar email (via provider.listCalendars inside
// exchangeCode), encrypts the refresh token with CALENDAR_KEK, upserts
// a calendar_connections row, and redirects to the calendar-selection page.
//
// No origin check: Google initiates this redirect; the Origin header is
// typically absent or "null". The state cookie + CSRF token comparison is
// the gate.
//
// See docs/features/calendar-binding/step-1-google-oauth-and-context.md
// AC1.27-AC1.33.

import { NextResponse } from 'next/server';
import {
  clearStateCookie,
  parseStateCookie,
  statesMatch,
} from '@/lib/auth/cal-oauth-state';
import { encrypt } from '@/lib/auth/envelope-encryption';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { getPublicOrigin } from '@/lib/auth/public-origin';
import { parseSessionCookie } from '@/lib/auth/session';
import { upsertConnection } from '@/lib/api/calendars';
import { getGoogleProvider } from '@/lib/integrations/google/get-provider';

const CALENDAR_READONLY_SCOPE =
  'https://www.googleapis.com/auth/calendar.readonly';

export async function GET(request: Request) {
  const requestUrl = new URL(request.url);
  const code = requestUrl.searchParams.get('code');
  const stateFromUrl = requestUrl.searchParams.get('state');

  // State cookie validation (CSRF protection)
  const stateFromCookie = parseStateCookie(request.headers.get('cookie'));
  if (!stateFromCookie) {
    return NextResponse.json({ error: 'state_missing' }, { status: 400 });
  }
  if (!stateFromUrl || !statesMatch(stateFromCookie, stateFromUrl)) {
    return NextResponse.json({ error: 'state_mismatch' }, { status: 400 });
  }
  if (!code) {
    return NextResponse.json({ error: 'missing_code' }, { status: 400 });
  }

  // Session validation (the user must have been logged in when they
  // started the connect flow)
  const sessionId = parseSessionCookie(request.headers.get('cookie'));
  if (!sessionId) {
    return NextResponse.json({ error: 'unauthenticated' }, { status: 401 });
  }
  const session = await getValidatedSession(sessionId);
  if (!session) {
    return NextResponse.json({ error: 'unauthenticated' }, { status: 401 });
  }

  // Resolve the user id. v1.6 is single-user; we read WILLEM_USER_ID
  // from env. v2 multi-user will look this up from the session.
  const userId = process.env.WILLEM_USER_ID;
  if (!userId) {
    return NextResponse.json({ error: 'server_error' }, { status: 500 });
  }

  // Exchange code for tokens + account email. Must use the same
  // redirect_uri that was sent to Google in the auth URL, which means
  // the public origin (not Node's internal 0.0.0.0:3000).
  const publicOrigin = getPublicOrigin(request);
  const redirectUri = `${publicOrigin}/api/calendars/google/callback`;
  let exchanged: {
    refreshToken: string;
    accessToken: string;
    expiresAt: Date;
    accountEmail: string;
  };
  try {
    const provider = getGoogleProvider();
    exchanged = await provider.exchangeCode(code, redirectUri);
  } catch {
    return NextResponse.json({ error: 'oauth_exchange_failed' }, { status: 502 });
  }

  // Encrypt refresh token
  const kek = process.env.CALENDAR_KEK;
  if (!kek) {
    return NextResponse.json({ error: 'server_error' }, { status: 500 });
  }
  let refreshTokenEncrypted: string;
  try {
    refreshTokenEncrypted = encrypt(exchanged.refreshToken, kek);
  } catch {
    return NextResponse.json({ error: 'server_error' }, { status: 500 });
  }

  // Upsert connection using the user's per-request Directus token
  // (session.accessToken). This is the same pattern as tags / episodes /
  // day-entries routes. The Fly `DIRECTUS_TOKEN` env var is the scoped
  // sessions-only-policy token — it has access to frontend_sessions ONLY,
  // not to calendar collections. session.accessToken belongs to the
  // gevoelscore-frontend-api policy which has CRUD on calendar_*.
  const upsertResult = await upsertConnection(session.accessToken, {
    user_id: userId,
    provider: 'google',
    provider_account_email: exchanged.accountEmail,
    refresh_token_encrypted: refreshTokenEncrypted,
    scope: CALENDAR_READONLY_SCOPE,
    connected_at: new Date().toISOString(),
  });
  if (!upsertResult.ok) {
    return NextResponse.json({ error: 'directus_error' }, { status: 502 });
  }
  const connectionId = upsertResult.value;

  // Redirect to the calendar-selection page + clear state cookie.
  // Same public-origin derivation: if we used requestUrl.origin here,
  // the browser would be sent to https://0.0.0.0:3000/... which is
  // unreachable.
  const response = NextResponse.redirect(
    `${publicOrigin}/settings/kalenders/choose?connection_id=${encodeURIComponent(connectionId)}`,
    302,
  );
  response.headers.set('Set-Cookie', clearStateCookie());
  return response;
}
