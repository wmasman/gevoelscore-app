// GET /api/day-entries?from=YYYY-MM-DD&to=YYYY-MM-DD
//
// Returns day_entries in the inclusive date range. Max range 90 days
// (server-side cap to keep payloads bounded and discourage accidental
// large reads). Permissive read rate-limit (S-M5, audit 2026-05-30):
// 120 / 5min / IP, defence-in-depth against a leaked session cookie
// being hammered.

import { NextResponse } from 'next/server';
import { readDayEntriesInRange } from '@/lib/api/day-entries';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { parseSessionCookie } from '@/lib/auth/session';
import { dayEntryReadRateLimiter, getClientIp } from '@/lib/auth/stores';
import { validateDate } from '@/lib/domain/date';

const MAX_RANGE_DAYS = 90;
const MS_PER_DAY = 24 * 60 * 60 * 1000;

function daysBetween(from: string, to: string): number {
  // Both inputs are already-validated YYYY-MM-DD strings. Treat as UTC
  // midnight to avoid DST drift in the delta.
  return Math.floor(
    (Date.parse(`${to}T00:00:00Z`) - Date.parse(`${from}T00:00:00Z`)) / MS_PER_DAY,
  );
}

export async function GET(request: Request) {
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

  const ip = getClientIp(request);
  const rl = dayEntryReadRateLimiter.check(ip);
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

  const url = new URL(request.url);
  const fromParam = url.searchParams.get('from');
  const toParam = url.searchParams.get('to');

  const fromResult = validateDate(fromParam);
  const toResult = validateDate(toParam);
  if (!fromResult.ok || !toResult.ok) {
    return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
  }
  const from = fromResult.value;
  const to = toResult.value;

  if (to < from) {
    return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
  }
  if (daysBetween(from, to) >= MAX_RANGE_DAYS) {
    return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
  }

  const result = await readDayEntriesInRange(session.accessToken, from, to);
  if (!result.ok) {
    return NextResponse.json({ error: 'server_error' }, { status: 502 });
  }

  return NextResponse.json({ entries: result.value }, { status: 200 });
}
