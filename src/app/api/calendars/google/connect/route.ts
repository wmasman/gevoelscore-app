// POST /api/calendars/google/connect — initiates the Google OAuth flow.
//
// Standard auth stack (origin → session → rate-limit). Generates a random
// state value, sets the cal_oauth_state cookie (httpOnly + Secure +
// SameSite=Lax + 10-min Max-Age), and returns the Google authorization URL
// for the client to redirect to.
//
// See docs/features/calendar-binding/step-1-google-oauth-and-context.md
// AC1.24-AC1.26.

import { NextResponse } from 'next/server';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import {
  buildStateCookie,
  generateOAuthState,
} from '@/lib/auth/cal-oauth-state';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { getPublicOrigin } from '@/lib/auth/public-origin';
import { parseSessionCookie } from '@/lib/auth/session';
import { calendarWriteRateLimiter, getClientIp } from '@/lib/auth/stores';
import { getGoogleProvider } from '@/lib/integrations/google/get-provider';

export async function POST(request: Request) {
  if (
    !validateOrigin(
      request.headers.get('origin'),
      request.headers.get('referer'),
      allowedOrigins(),
      request.method,
    )
  ) {
    return NextResponse.json({ error: 'forbidden' }, { status: 403 });
  }

  const sessionId = parseSessionCookie(request.headers.get('cookie'));
  if (!sessionId) {
    return NextResponse.json({ error: 'unauthenticated' }, { status: 401 });
  }
  const session = await getValidatedSession(sessionId);
  if (!session) {
    return NextResponse.json({ error: 'unauthenticated' }, { status: 401 });
  }

  const ip = getClientIp(request);
  const rl = calendarWriteRateLimiter.check(ip);
  if (!rl.allowed) {
    return NextResponse.json(
      { error: 'rate_limited', retry_after_ms: rl.retryAfterMs },
      { status: 429 },
    );
  }

  const state = generateOAuthState();
  // Derive the public origin from headers — request.url reflects Node's
  // internal listen address (0.0.0.0:3000) when behind Fly's edge proxy.
  // See src/lib/auth/public-origin.ts for the resolution priority.
  const redirectUri = `${getPublicOrigin(request)}/api/calendars/google/callback`;

  let redirectUrl: string;
  try {
    const provider = getGoogleProvider();
    redirectUrl = provider.buildAuthUrl(state, redirectUri);
  } catch {
    return NextResponse.json({ error: 'server_error' }, { status: 500 });
  }

  const response = NextResponse.json(
    { redirect_url: redirectUrl },
    { status: 200 },
  );
  response.headers.set('Set-Cookie', buildStateCookie(state));
  return response;
}
