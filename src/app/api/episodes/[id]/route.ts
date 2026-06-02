// PATCH /api/episodes/[id]
//
// Updates an existing episode. Partial body semantics — any non-empty
// subset of { label, category, start_date, end_date, description,
// archived_at } is accepted. archived_at: ISO archives; archived_at:
// null un-archives. Standard gate stack: origin → rate-limit → session
// → UUID-format check → body parse → SDK wrapper → error mapping.
//
// Per AC9a in step-2 plan: the [id] path param is validated as a
// UUID-shape string at this boundary before the SDK is reached.
// Defense-in-depth — non-UUID input never reaches Directus, never
// gets reflected into error paths.

import { NextResponse } from 'next/server';
import { updateEpisode } from '@/lib/api/episodes';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { parseSessionCookie } from '@/lib/auth/session';
import {
  episodeWriteRateLimiter,
  getClientIp,
} from '@/lib/auth/stores';

// Standard UUID v4-ish shape: 8-4-4-4-12 hex digits with dashes.
// Liberal on the case + version byte — Directus generates v4 UUIDs but
// the goal here is "is this a UUID-looking thing?" not "is this exactly
// RFC 4122 v4?". A non-conforming UUID rejected here is fine; a malicious
// non-UUID slipping through is the failure mode we're guarding against.
const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

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

  const ip = getClientIp(request);
  const rl = episodeWriteRateLimiter.check(ip);
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

  const { id: rawId } = await context.params;
  if (!UUID_REGEX.test(rawId)) {
    return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
  }

  // Coarse body parse — the SDK wrapper does strict per-field validation.
  let body: Record<string, unknown>;
  try {
    body = (await request.json()) as Record<string, unknown>;
  } catch {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }
  if (typeof body !== 'object' || body === null || Array.isArray(body)) {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }

  // Build the patch from the keys present in the body. Only known keys
  // are forwarded; anything else is silently dropped (defence against
  // a client trying to set internal fields like id / created_at).
  const patch: Parameters<typeof updateEpisode>[2] = {};
  if ('label' in body) patch.label = body.label as string;
  if ('category' in body) patch.category = body.category as never;
  if ('start_date' in body) patch.start_date = body.start_date as string;
  if ('end_date' in body) patch.end_date = body.end_date as string | null;
  if ('description' in body) patch.description = body.description as string | null;
  if ('archived_at' in body) patch.archived_at = body.archived_at as string | null;

  if (Object.keys(patch).length === 0) {
    return NextResponse.json({ error: 'empty_patch' }, { status: 400 });
  }

  const result = await updateEpisode(session.accessToken, rawId, patch);

  if (!result.ok) {
    if (
      result.error === 'invalid_label' ||
      result.error === 'invalid_category' ||
      result.error === 'invalid_date_range' ||
      result.error === 'invalid_description' ||
      result.error === 'invalid_archived_at' ||
      result.error === 'empty_patch'
    ) {
      return NextResponse.json({ error: result.error }, { status: 400 });
    }
    if (result.error === 'not_found') {
      return NextResponse.json({ error: 'not_found' }, { status: 404 });
    }
    return NextResponse.json({ error: 'server_error' }, { status: 502 });
  }

  return NextResponse.json({ episode: result.value }, { status: 200 });
}
