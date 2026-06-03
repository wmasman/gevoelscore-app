// PATCH + DELETE /api/tags/[id]
//
// PATCH (step-5 link/unlink + step v1.5b rename/recategorize/archive):
//   Body: any subset of { label, category, archived_at, parent_episode_id }
//   200:  { tag: Tag }
//   400:  { error: 'invalid_id' | 'malformed_body' | 'invalid_patch'
//                 | 'invalid_label' | 'invalid_category'
//                 | 'invalid_archived_at' | 'invalid_parent_episode_id' }
//   401:  { error: 'unauthenticated' }
//   403:  { error: 'forbidden' }
//   429:  { error: 'rate_limited', retry_after_ms: number }
//   502:  { error: 'server_error' }
//
// DELETE (step v1.5b tag-management-settings hard-delete):
//   Body: empty.
//   200:  { deleted_id: string }
//   400:  { error: 'invalid_id' | 'tag_in_use', usage_count?: number }
//   401:  { error: 'unauthenticated' }
//   403:  { error: 'forbidden' }
//   429:  { error: 'rate_limited', retry_after_ms: number }
//   502:  { error: 'server_error' }  (also for non-existent UUID — read fails)
//
// Both methods share the same auth stack: origin → session → rate-limit
// → UUID-format gate. DELETE additionally reads the row first to gate
// hard-delete on usage_count === 0 (the logical-FK guard against
// day_entries.tag_ids[]).

import { NextResponse } from 'next/server';
import { deleteTag, readTagById, updateTag } from '@/lib/api/tags';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { parseSessionCookie } from '@/lib/auth/session';
import { getClientIp, tagWriteRateLimiter } from '@/lib/auth/stores';
import { isUuidShape } from '@/lib/domain/uuid';

// Per-field error variants from updateTag that map 1:1 to a 400 response
// with the same code. The UI uses these to point the user at the
// specific field that failed validation.
const FIELD_LEVEL_ERRORS = new Set([
  'invalid_label',
  'invalid_category',
  'invalid_archived_at',
  'invalid_parent_episode_id',
] as const);

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
  // and per-field validation. Single source of truth lives there; the
  // route only maps lib errors to HTTP codes.
  const result = await updateTag(session.accessToken, rawId, body as never);

  if (!result.ok) {
    if (result.error === 'invalid_patch') {
      return NextResponse.json({ error: 'invalid_patch' }, { status: 400 });
    }
    if (FIELD_LEVEL_ERRORS.has(result.error as never)) {
      return NextResponse.json({ error: result.error }, { status: 400 });
    }
    return NextResponse.json({ error: 'server_error' }, { status: 502 });
  }

  return NextResponse.json({ tag: result.value }, { status: 200 });
}

export async function DELETE(
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

  // Read-then-delete with the usage_count gate. A non-existent UUID
  // surfaces here as directus_error from readTagById → 502 (M5: matches
  // the PATCH non-existent-UUID path). A usage_count > 0 means the tag
  // is referenced from at least one day_entry — refuse the delete and
  // surface the count so the UI can tell the user why.
  // TOCTOU: single-user single-device app makes the read-then-delete
  // race functionally impossible; documented as a known multi-user
  // follow-up.
  const readResult = await readTagById(session.accessToken, rawId);
  if (!readResult.ok) {
    return NextResponse.json({ error: 'server_error' }, { status: 502 });
  }
  if (readResult.value.usage_count > 0) {
    return NextResponse.json(
      {
        error: 'tag_in_use',
        usage_count: readResult.value.usage_count,
      },
      { status: 400 },
    );
  }

  const deleteResult = await deleteTag(session.accessToken, rawId);
  if (!deleteResult.ok) {
    return NextResponse.json({ error: 'server_error' }, { status: 502 });
  }

  return NextResponse.json(deleteResult.value, { status: 200 });
}
