// POST /api/tags — inline tag creation (2026-06-01).
//
// Body: { label: string, category: TagCategory }
// 200:  { outcome: 'created'|'matched_active'|'matched_reactivated', tag: Tag }
// 400:  { error: 'malformed_body'|'invalid_label'|'invalid_category' }
// 401:  { error: 'unauthenticated' }
// 403:  { error: 'forbidden' }
// 429:  { error: 'rate_limited', retry_after_ms: number }
// 502:  { error: 'server_error' }
//
// Single-purpose: this route does NOT touch day_entries. The client chains
// into the existing PUT /api/day-entries/[date] to attach the new tag-id —
// keeps the API contract clean and the existing tag-attach code path the
// single source of truth (see B1 + M3 in the step-1 audit).
//
// No admin/static token is used. The user's session.accessToken is passed
// to createOrUpsertTag; Directus enforces collection permissions based on
// the user's role at the moment of the call.

import { NextResponse } from 'next/server';
import { createOrUpsertTag } from '@/lib/api/tags';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { parseSessionCookie } from '@/lib/auth/session';
import { getClientIp, tagWriteRateLimiter } from '@/lib/auth/stores';

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
  const rl = tagWriteRateLimiter.check(ip);
  if (!rl.allowed) {
    return NextResponse.json(
      { error: 'rate_limited', retry_after_ms: rl.retryAfterMs },
      { status: 429 },
    );
  }

  let body: { label?: unknown; category?: unknown };
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }

  if (typeof body !== 'object' || body === null) {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }
  if (typeof body.label !== 'string' || typeof body.category !== 'string') {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }

  const result = await createOrUpsertTag(session.accessToken, {
    label: body.label,
    // `createOrUpsertTag` runs `validateTagCategory` itself; the cast here
    // is a parser convenience, not a trust-the-client assertion.
    category: body.category as never,
  });

  if (!result.ok) {
    if (result.error === 'invalid_label') {
      return NextResponse.json({ error: 'invalid_label' }, { status: 400 });
    }
    if (result.error === 'invalid_category') {
      return NextResponse.json({ error: 'invalid_category' }, { status: 400 });
    }
    return NextResponse.json({ error: 'server_error' }, { status: 502 });
  }

  return NextResponse.json(
    { outcome: result.value.kind, tag: result.value.tag },
    { status: 200 },
  );
}
