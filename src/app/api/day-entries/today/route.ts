// GET /api/day-entries/today
//
// Returns the user's day_entry for today's Europe/Amsterdam date.
// Response: { entry: DayEntry | null }. Null = no row logged today.
//
// Read-only; permissive shared rate-limit (S-M5: 120 / 5min / IP via
// dayEntryReadRateLimiter). Authentication is enforced by middleware
// plus the route's own getValidatedSession call as defense in depth.

import { NextResponse } from 'next/server';
import { readDayEntryByDate } from '@/lib/api/day-entries';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { parseSessionCookie } from '@/lib/auth/session';
import { dayEntryReadRateLimiter, getClientIp } from '@/lib/auth/stores';
import { todayInAmsterdam } from '@/lib/domain/date';

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

  const today = todayInAmsterdam();
  const result = await readDayEntryByDate(session.accessToken, today);
  if (!result.ok) {
    return NextResponse.json({ error: 'server_error' }, { status: 502 });
  }

  return NextResponse.json({ entry: result.value }, { status: 200 });
}
