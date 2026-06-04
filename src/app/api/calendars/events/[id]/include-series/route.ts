// POST /api/calendars/events/[id]/include-series
//
// Symmetric coarse re-include: re-includes the entire series (all sibling
// events sharing the path event's recurrence_id). Used by the
// "Voeg hele serie weer toe" button in the per-event detail sheet.
//
// Order: DELETE the series_exclusion row FIRST (so future pulls of the
// recurrence default back to included), THEN bulk PATCH all current
// sibling events.
//
// See docs/features/calendar-binding/step-1-google-oauth-and-context.md
// AC1.50-AC1.52.

import { NextResponse } from 'next/server';
import {
  deleteSeriesExclusion,
  patchCalendarEventsBulk,
  readCalendarEventById,
  readConnectionById,
  readEventsByRecurrenceId,
} from '@/lib/api/calendars';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { parseSessionCookie } from '@/lib/auth/session';
import { calendarWriteRateLimiter, getClientIp } from '@/lib/auth/stores';
import { isUuidShape } from '@/lib/domain/uuid';

type Context = { params: Promise<{ id: string }> };

export async function POST(request: Request, context: Context) {
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

  const userId = process.env.WILLEM_USER_ID;
  const adminToken = process.env.DIRECTUS_TOKEN;
  if (!userId || !adminToken) {
    return NextResponse.json({ error: 'server_error' }, { status: 500 });
  }

  const { id } = await context.params;
  if (!isUuidShape(id)) {
    return NextResponse.json({ error: 'invalid_id' }, { status: 400 });
  }

  const eventResult = await readCalendarEventById(adminToken, id);
  if (!eventResult.ok) {
    return NextResponse.json({ error: 'directus_error' }, { status: 502 });
  }
  if (!eventResult.value) {
    return NextResponse.json({ error: 'not_found' }, { status: 404 });
  }
  const event = eventResult.value;
  if (event.recurrence_id === null) {
    return NextResponse.json(
      { error: 'event_not_recurring' },
      { status: 400 },
    );
  }

  const connResult = await readConnectionById(adminToken, event.connection_id);
  if (!connResult.ok) {
    return NextResponse.json({ error: 'directus_error' }, { status: 502 });
  }
  if (!connResult.value || connResult.value.user_id !== userId) {
    return NextResponse.json({ error: 'forbidden' }, { status: 403 });
  }

  // 1. DELETE the series_exclusion row.
  const deleteResult = await deleteSeriesExclusion(
    adminToken,
    event.connection_id,
    event.recurrence_id,
  );
  if (!deleteResult.ok) {
    return NextResponse.json({ error: 'directus_error' }, { status: 502 });
  }

  // 2. Bulk PATCH all sibling events.
  const siblingsResult = await readEventsByRecurrenceId(
    adminToken,
    event.connection_id,
    event.recurrence_id,
  );
  if (!siblingsResult.ok) {
    return NextResponse.json({ error: 'directus_error' }, { status: 502 });
  }
  const ids = siblingsResult.value.map((r) => r.id);
  const bulkResult = await patchCalendarEventsBulk(adminToken, ids, {
    included_as_context: true,
    user_decision: 'user_included',
  });
  if (!bulkResult.ok) {
    return NextResponse.json({ error: 'directus_error' }, { status: 502 });
  }

  return NextResponse.json(
    {
      recurrence_id: event.recurrence_id,
      events_updated: ids.length,
    },
    { status: 200 },
  );
}
