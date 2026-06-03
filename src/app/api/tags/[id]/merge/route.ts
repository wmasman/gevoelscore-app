// POST /api/tags/[id]/merge — step v1.5c.
//
// Body:   { target_tag_id: string }
// 200:    { source_id, target_id, affected_days }
// 400:    'invalid_id' | 'malformed_body' | 'invalid_target' | 'same_tag'
//          | 'source_not_found' | 'target_not_found'
//          | 'source_archived' | 'target_archived' | 'category_mismatch'
// 401:    'unauthenticated'
// 403:    'forbidden'
// 429:    'rate_limited'
// 502:    'server_error'
//
// Shares the same auth stack as the other tag routes: origin → session →
// rate-limit (tagWriteRateLimiter) → UUID-format gate on path id → body
// parse + UUID-format gate on `target_tag_id` → mergeTag lib call.

import { NextResponse } from 'next/server';
import { mergeTag } from '@/lib/api/tags';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { parseSessionCookie } from '@/lib/auth/session';
import { getClientIp, tagWriteRateLimiter } from '@/lib/auth/stores';
import { isUuidShape } from '@/lib/domain/uuid';

// Lib MergeTagError variants that map 1:1 to a 400 response with the
// same code. The UI uses these to surface a specific reason. Anything
// else (network_error / directus_error) becomes 502 server_error.
const FOUR_HUNDRED_LIB_ERRORS = new Set([
  'same_tag',
  'source_not_found',
  'target_not_found',
  'source_archived',
  'target_archived',
  'category_mismatch',
]);

export async function POST(
  request: Request,
  context: { params: Promise<{ id: string }> },
) {
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

  const { id: rawId } = await context.params;
  if (!isUuidShape(rawId)) {
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

  const targetTagId = body.target_tag_id;
  if (typeof targetTagId !== 'string') {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }
  if (!isUuidShape(targetTagId)) {
    return NextResponse.json({ error: 'invalid_target' }, { status: 400 });
  }

  const result = await mergeTag(session.accessToken, rawId, targetTagId);

  if (!result.ok) {
    if (FOUR_HUNDRED_LIB_ERRORS.has(result.error)) {
      return NextResponse.json({ error: result.error }, { status: 400 });
    }
    return NextResponse.json({ error: 'server_error' }, { status: 502 });
  }

  return NextResponse.json(result.value, { status: 200 });
}
