// PATCH /api/tags/[id] — step-5 tag-to-episode linking.
//
// Body: { parent_episode_id: string | null }
// 200:  { tag: Tag }
// 400:  { error: 'invalid_id' | 'malformed_body' | 'invalid_patch' }
// 401:  { error: 'unauthenticated' }
// 403:  { error: 'forbidden' }
// 429:  { error: 'rate_limited', retry_after_ms: number }
// 502:  { error: 'server_error' }
//
// Single-purpose: this route only re-parents (link / unlink). Label and
// category changes for tags go through tag-management-settings in v1.5b.
// The [id] path param is gated as UUID-shape before the SDK is reached —
// defense-in-depth so malformed input never touches Directus.

import { NextResponse } from 'next/server';
import { updateTag } from '@/lib/api/tags';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { parseSessionCookie } from '@/lib/auth/session';
import { getClientIp, tagWriteRateLimiter } from '@/lib/auth/stores';
import { isUuidShape } from '@/lib/domain/uuid';

export async function PATCH(
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

  // Forward the body verbatim — updateTag enforces the allowed-key gate
  // and runs validateParentEpisodeId. Single source of truth lives there;
  // the route only normalises HTTP shape.
  const result = await updateTag(session.accessToken, rawId, body as never);

  if (!result.ok) {
    if (result.error === 'invalid_patch') {
      return NextResponse.json({ error: 'invalid_patch' }, { status: 400 });
    }
    return NextResponse.json({ error: 'server_error' }, { status: 502 });
  }

  return NextResponse.json({ tag: result.value }, { status: 200 });
}
