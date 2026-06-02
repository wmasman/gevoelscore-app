// GET /api/episodes        — list active episodes, sorted by start_date DESC
// GET /api/episodes?archived=all — include archived episodes in the response
// POST /api/episodes       — create an episode
//
// Mirrors /api/tags and /api/day-entries route handlers: standard gate
// order (origin → rate-limit → session → request validation → SDK wrapper
// → error mapping). Body validation is coarse here (typeof checks); the
// SDK wrapper runs the domain validators. Error responses do not echo
// input back — generic per-variant strings only.

import { NextResponse } from 'next/server';
import { createEpisode, readAllEpisodes } from '@/lib/api/episodes';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { parseSessionCookie } from '@/lib/auth/session';
import {
  episodeReadRateLimiter,
  episodeWriteRateLimiter,
  getClientIp,
} from '@/lib/auth/stores';

// ---------------------------------------------------------------------------
// GET — list episodes
// ---------------------------------------------------------------------------

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
  const rl = episodeReadRateLimiter.check(ip);
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

  // Query param: ?archived=all OR absent. Any other value is rejected
  // explicitly so a typo'd `?archived=true` doesn't quietly fall through
  // to default behaviour.
  const url = new URL(request.url);
  const archivedParam = url.searchParams.get('archived');
  let includeArchived = false;
  if (archivedParam !== null) {
    if (archivedParam !== 'all') {
      return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
    }
    includeArchived = true;
  }

  const result = await readAllEpisodes(session.accessToken, { includeArchived });
  if (!result.ok) {
    return NextResponse.json({ error: 'server_error' }, { status: 502 });
  }

  return NextResponse.json({ episodes: result.value }, { status: 200 });
}

// ---------------------------------------------------------------------------
// POST — create episode
// ---------------------------------------------------------------------------

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

  // Coarse body parse — the SDK wrapper does strict per-field validation.
  let body: {
    label?: unknown;
    category?: unknown;
    start_date?: unknown;
    end_date?: unknown;
    description?: unknown;
  };
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }
  if (typeof body !== 'object' || body === null) {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }
  if (
    typeof body.label !== 'string' ||
    typeof body.category !== 'string' ||
    typeof body.start_date !== 'string'
  ) {
    return NextResponse.json({ error: 'malformed_body' }, { status: 400 });
  }

  const result = await createEpisode(session.accessToken, {
    label: body.label,
    // The wrapper runs validateEpisodeCategory; the cast is a parser
    // convenience, not a trust-the-client assertion.
    category: body.category as never,
    start_date: body.start_date,
    end_date: body.end_date as string | null | undefined,
    description: body.description as string | null | undefined,
  });

  if (!result.ok) {
    if (
      result.error === 'invalid_label' ||
      result.error === 'invalid_category' ||
      result.error === 'invalid_date_range' ||
      result.error === 'invalid_description'
    ) {
      return NextResponse.json({ error: result.error }, { status: 400 });
    }
    return NextResponse.json({ error: 'server_error' }, { status: 502 });
  }

  return NextResponse.json({ episode: result.value }, { status: 200 });
}
