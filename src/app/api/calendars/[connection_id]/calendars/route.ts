// GET + POST /api/calendars/[connection_id]/calendars
//
// GET: lists the user's Google calendars after the OAuth callback so the
// post-connect screen can show them for selection. Refreshes the access
// token from the stored encrypted refresh token, then calls
// provider.listCalendars.
//
// POST: persists the user's per-calendar inclusion choice into
// calendar_connections.included_calendar_ids. The immediate sync trigger
// (AC1.35) is deferred to Phase 1.D when the event-CRUD wrappers exist;
// for v1.6 ship-1.C, the user clicks `Ververs nu` to pull events after
// selecting calendars.
//
// See docs/features/calendar-binding/step-1-google-oauth-and-context.md
// AC1.34-AC1.35.

import { NextResponse } from 'next/server';
import {
  patchConnection,
  readConnectionById,
} from '@/lib/api/calendars';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import { decrypt } from '@/lib/auth/envelope-encryption';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { parseSessionCookie } from '@/lib/auth/session';
import { calendarWriteRateLimiter, getClientIp } from '@/lib/auth/stores';
import { isUuidShape } from '@/lib/domain/uuid';
import { getGoogleProvider } from '@/lib/integrations/google/get-provider';

type Context = { params: Promise<{ connection_id: string }> };

async function authenticate(
  request: Request,
): Promise<
  | { ok: true; userId: string; accessToken: string }
  | { ok: false; response: Response }
> {
  if (
    !validateOrigin(
      request.headers.get('origin'),
      request.headers.get('referer'),
      allowedOrigins(),
      request.method,
    )
  ) {
    return {
      ok: false,
      response: NextResponse.json({ error: 'forbidden' }, { status: 403 }),
    };
  }
  const sessionId = parseSessionCookie(request.headers.get('cookie'));
  if (!sessionId) {
    return {
      ok: false,
      response: NextResponse.json({ error: 'unauthenticated' }, { status: 401 }),
    };
  }
  const session = await getValidatedSession(sessionId);
  if (!session) {
    return {
      ok: false,
      response: NextResponse.json({ error: 'unauthenticated' }, { status: 401 }),
    };
  }
  const userId = process.env.WILLEM_USER_ID;
  if (!userId) {
    return {
      ok: false,
      response: NextResponse.json({ error: 'server_error' }, { status: 500 }),
    };
  }
  // Use session.accessToken (user's per-request token tied to the
  // gevoelscore-frontend-api policy) for Directus calls — NOT the
  // scoped sessions-only DIRECTUS_TOKEN env var.
  return { ok: true, userId, accessToken: session.accessToken };
}

async function resolveConnectionOrFail(
  rawId: string,
  userId: string,
  accessToken: string,
): Promise<
  | { ok: true; connection: import('@/lib/api/calendars').DirectusCalendarConnectionRow }
  | { ok: false; response: Response }
> {
  if (!isUuidShape(rawId)) {
    return {
      ok: false,
      response: NextResponse.json({ error: 'invalid_id' }, { status: 400 }),
    };
  }
  const connResult = await readConnectionById(accessToken, rawId);
  if (!connResult.ok) {
    return {
      ok: false,
      response: NextResponse.json({ error: 'directus_error' }, { status: 502 }),
    };
  }
  if (!connResult.value) {
    return {
      ok: false,
      response: NextResponse.json({ error: 'not_found' }, { status: 404 }),
    };
  }
  if (connResult.value.user_id !== userId) {
    return {
      ok: false,
      response: NextResponse.json({ error: 'forbidden' }, { status: 403 }),
    };
  }
  return { ok: true, connection: connResult.value };
}

export async function GET(request: Request, context: Context) {
  const auth = await authenticate(request);
  if (!auth.ok) return auth.response;
  const { userId, accessToken } = auth;

  const ip = getClientIp(request);
  const rl = calendarWriteRateLimiter.check(ip);
  if (!rl.allowed) {
    return NextResponse.json(
      { error: 'rate_limited', retry_after_ms: rl.retryAfterMs },
      { status: 429 },
    );
  }

  const { connection_id } = await context.params;
  const resolved = await resolveConnectionOrFail(
    connection_id,
    userId,
    accessToken,
  );
  if (!resolved.ok) return resolved.response;
  const { connection } = resolved;

  const kek = process.env.CALENDAR_KEK;
  if (!kek) {
    return NextResponse.json({ error: 'server_error' }, { status: 500 });
  }

  let calendars: Awaited<
    ReturnType<import('@/lib/integrations/calendar-provider').CalendarProvider['listCalendars']>
  >;
  try {
    const refreshToken = decrypt(connection.refresh_token_encrypted, kek);
    const provider = getGoogleProvider();
    const refreshed = await provider.refreshAccessToken(refreshToken);
    calendars = await provider.listCalendars(refreshed.accessToken);
  } catch {
    return NextResponse.json({ error: 'provider_error' }, { status: 502 });
  }

  return NextResponse.json({ calendars }, { status: 200 });
}

export async function POST(request: Request, context: Context) {
  const auth = await authenticate(request);
  if (!auth.ok) return auth.response;
  const { userId, accessToken } = auth;

  const ip = getClientIp(request);
  const rl = calendarWriteRateLimiter.check(ip);
  if (!rl.allowed) {
    return NextResponse.json(
      { error: 'rate_limited', retry_after_ms: rl.retryAfterMs },
      { status: 429 },
    );
  }

  const { connection_id } = await context.params;
  const resolved = await resolveConnectionOrFail(
    connection_id,
    userId,
    accessToken,
  );
  if (!resolved.ok) return resolved.response;

  let body: Record<string, unknown>;
  try {
    body = (await request.json()) as Record<string, unknown>;
  } catch {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }
  if (typeof body !== 'object' || body === null || Array.isArray(body)) {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }

  const ids = body.included_calendar_ids;
  if (!Array.isArray(ids) || ids.some((id) => typeof id !== 'string')) {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }

  const patchResult = await patchConnection(accessToken, connection_id, {
    included_calendar_ids: ids as string[],
  });
  if (!patchResult.ok) {
    return NextResponse.json({ error: 'directus_error' }, { status: 502 });
  }

  // AC1.35: immediate-sync trigger deferred to Phase 1.D when the event
  // CRUD wrappers (readEventsByProviderIds, createCalendarEvent,
  // updateCalendarEvent, readSeriesExclusions) exist. For now, the user
  // clicks `Ververs nu` on Settings to populate events.
  return NextResponse.json(
    { ok: true, included_calendar_ids: ids },
    { status: 200 },
  );
}
