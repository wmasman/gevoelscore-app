// PATCH /api/calendars/events/[id]
//
// Updates a calendar_event row. Body shape (all optional):
//   - linked_tag_id: string | null
//   - linked_episode_id: string | null
//   - included_as_context: boolean
//
// Side effect on included_as_context=false for a recurring event
// (recurrence_id !== null):
//   - INSERTs into calendar_series_exclusions (idempotent)
//   - bulk PATCHes all sibling events to included_as_context=false +
//     user_decision=user_excluded
// Order: INSERT exclusion FIRST so the rule is durable even if the
// bulk PATCH fails mid-way.
//
// For included_as_context=true on a recurring event:
//   - per-row update only; series exclusion is NOT deleted (asymmetric
//     re-include — coarse exclude, fine re-include).
//
// See docs/features/calendar-binding/step-1-google-oauth-and-context.md
// AC1.44-AC1.49.

import { NextResponse } from 'next/server';
import {
  insertSeriesExclusion,
  patchCalendarEvent,
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

export async function PATCH(request: Request, context: Context) {
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
  if (!userId) {
    return NextResponse.json({ error: 'server_error' }, { status: 500 });
  }
  // session.accessToken (user's per-request token, scoped to
  // gevoelscore-frontend-api policy) — NOT DIRECTUS_TOKEN env var, which
  // is the sessions-only-policy token.
  const accessToken = session.accessToken;

  const { id } = await context.params;
  if (!isUuidShape(id)) {
    return NextResponse.json({ error: 'invalid_id' }, { status: 400 });
  }

  let body: Record<string, unknown>;
  try {
    body = (await request.json()) as Record<string, unknown>;
  } catch {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }
  if (typeof body !== 'object' || body === null || Array.isArray(body)) {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }

  // Validate optional fields.
  const linkedTagId =
    body.linked_tag_id === null || body.linked_tag_id === undefined
      ? body.linked_tag_id
      : typeof body.linked_tag_id === 'string' && isUuidShape(body.linked_tag_id)
        ? body.linked_tag_id
        : undefined;
  if (linkedTagId === undefined && 'linked_tag_id' in body) {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }

  const linkedEpisodeId =
    body.linked_episode_id === null || body.linked_episode_id === undefined
      ? body.linked_episode_id
      : typeof body.linked_episode_id === 'string' &&
          isUuidShape(body.linked_episode_id)
        ? body.linked_episode_id
        : undefined;
  if (linkedEpisodeId === undefined && 'linked_episode_id' in body) {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }

  const includedAsContext =
    body.included_as_context === undefined
      ? undefined
      : typeof body.included_as_context === 'boolean'
        ? body.included_as_context
        : 'INVALID';
  if (includedAsContext === 'INVALID') {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }

  // Ownership: read event → connection → user_id check.
  const eventResult = await readCalendarEventById(accessToken, id);
  if (!eventResult.ok) {
    return NextResponse.json({ error: 'directus_error' }, { status: 502 });
  }
  if (!eventResult.value) {
    return NextResponse.json({ error: 'not_found' }, { status: 404 });
  }
  const event = eventResult.value;
  const connResult = await readConnectionById(accessToken, event.connection_id);
  if (!connResult.ok) {
    return NextResponse.json({ error: 'directus_error' }, { status: 502 });
  }
  if (!connResult.value || connResult.value.user_id !== userId) {
    return NextResponse.json({ error: 'forbidden' }, { status: 403 });
  }

  // Build the per-row patch.
  const patch: Partial<import('@/lib/api/calendars').DirectusCalendarEventRow> = {};
  if ('linked_tag_id' in body) patch.linked_tag_id = linkedTagId as string | null;
  if ('linked_episode_id' in body)
    patch.linked_episode_id = linkedEpisodeId as string | null;
  if (includedAsContext !== undefined) {
    patch.included_as_context = includedAsContext;
    patch.user_decision = includedAsContext ? 'user_included' : 'user_excluded';
  }

  // Series-level side effect: included_as_context=false on a recurring
  // event triggers series-wide exclusion.
  const isRecurring = event.recurrence_id !== null;
  if (
    includedAsContext === false &&
    isRecurring &&
    event.recurrence_id !== null
  ) {
    // 1. Insert exclusion FIRST (durable rule).
    const insertResult = await insertSeriesExclusion(
      accessToken,
      event.connection_id,
      event.recurrence_id,
      new Date().toISOString(),
    );
    if (!insertResult.ok) {
      return NextResponse.json({ error: 'directus_error' }, { status: 502 });
    }

    // 2. Bulk PATCH all siblings.
    const siblingsResult = await readEventsByRecurrenceId(
      accessToken,
      event.connection_id,
      event.recurrence_id,
    );
    if (!siblingsResult.ok) {
      return NextResponse.json({ error: 'directus_error' }, { status: 502 });
    }
    const bulkResult = await patchCalendarEventsBulk(
      accessToken,
      siblingsResult.value.map((r) => r.id),
      {
        included_as_context: false,
        user_decision: 'user_excluded',
      },
    );
    if (!bulkResult.ok) {
      return NextResponse.json({ error: 'directus_error' }, { status: 502 });
    }
  } else if (Object.keys(patch).length > 0) {
    // Plain per-row patch (linked_tag/episode + per-row include flip).
    const patchResult = await patchCalendarEvent(accessToken, id, patch);
    if (!patchResult.ok) {
      return NextResponse.json({ error: 'directus_error' }, { status: 502 });
    }
  }

  return NextResponse.json(
    {
      id,
      linked_tag_id: patch.linked_tag_id ?? event.linked_tag_id,
      linked_episode_id: patch.linked_episode_id ?? event.linked_episode_id,
      included_as_context:
        patch.included_as_context ?? event.included_as_context,
      user_decision: patch.user_decision ?? event.user_decision,
    },
    { status: 200 },
  );
}
