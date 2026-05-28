// PUT /api/day-entries/[date]
//
// Upserts a day_entry keyed by date. Single endpoint for both today and
// past-day edits (timeline bottom sheet in Step 6 hits the same path with
// the tapped date). The route handler validates the date + body via the
// domain validators, runs the standard origin + rate-limit + auth gates,
// then delegates the actual write to upsertDayEntry().

import { NextResponse } from 'next/server';
import { upsertDayEntry } from '@/lib/api/day-entries';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { parseSessionCookie } from '@/lib/auth/session';
import { dayEntryWriteRateLimiter, getClientIp } from '@/lib/auth/stores';
import { validateDate } from '@/lib/domain/date';
import { normalizeNote } from '@/lib/domain/note';
import { validateScore, type Score } from '@/lib/domain/score';
import { validateTagIds } from '@/lib/domain/tag-ids';

export async function PUT(
  request: Request,
  context: { params: Promise<{ date: string }> },
) {
  if (
    !validateOrigin(
      request.headers.get('origin'),
      request.headers.get('referer'),
      allowedOrigins(),
    )
  ) {
    return NextResponse.json({ error: 'forbidden' }, { status: 403 });
  }

  const ip = getClientIp(request);
  const rl = dayEntryWriteRateLimiter.check(ip);
  if (!rl.allowed) {
    return NextResponse.json(
      { error: 'rate_limited', retry_after_ms: rl.retryAfterMs },
      { status: 429 },
    );
  }

  const sessionId = parseSessionCookie(request.headers.get('cookie'));
  if (!sessionId) {
    return NextResponse.json({ error: 'unauthenticated' }, { status: 401 });
  }
  const session = await getValidatedSession(sessionId);
  if (!session) {
    return NextResponse.json({ error: 'unauthenticated' }, { status: 401 });
  }

  const { date: rawDate } = await context.params;
  const dateResult = validateDate(rawDate);
  if (!dateResult.ok) {
    return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
  }

  let body: { score?: unknown; note?: unknown; tag_ids?: unknown };
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
  }

  // Build the patch from whichever fields the caller supplied. PUT is
  // upsert-by-date with partial-update semantics: NoteField sends
  // `{ note: ... }`, TagCategoryList sends `{ tag_ids: [...] }`, the
  // wheel sends `{ score: N }`. The empty patch is invalid (nothing to
  // do). Score is REQUIRED only when the row doesn't exist yet — the
  // SDK wrapper signals that via 'missing_score_for_create'.
  const patch: { score?: Score; note?: string | null; tag_ids?: string[] } = {};

  if ('score' in body) {
    const scoreResult = validateScore(body.score);
    if (!scoreResult.ok) {
      return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
    }
    patch.score = scoreResult.value;
  }

  if ('note' in body) {
    const noteResult = normalizeNote(body.note);
    if (!noteResult.ok) {
      return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
    }
    patch.note = noteResult.value;
  }

  if ('tag_ids' in body) {
    const tagIdsResult = validateTagIds(body.tag_ids);
    if (!tagIdsResult.ok) {
      return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
    }
    patch.tag_ids = tagIdsResult.value;
  }

  if (Object.keys(patch).length === 0) {
    return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
  }

  // TODO(I3): audit-log entry — { timestamp, event: 'day_entry_upsert',
  // outcome, ip-hashed, date } per NEN 7510 §12.4 once the
  // directus_auth_events collection lands in Track A3.

  const result = await upsertDayEntry(session.accessToken, dateResult.value, patch);
  if (!result.ok) {
    if (result.error === 'missing_score_for_create') {
      return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
    }
    return NextResponse.json({ error: 'server_error' }, { status: 502 });
  }

  return NextResponse.json({ entry: result.value }, { status: 200 });
}
