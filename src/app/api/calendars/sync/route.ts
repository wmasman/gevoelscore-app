// POST /api/calendars/sync
//
// Two auth paths share one code path:
//   - Session: parseSessionCookie + getValidatedSession; iterates the
//     session-user's active connections.
//   - Bearer: constant-time CALENDAR_SYNC_SECRET match; iterates ALL
//     active connections (system scope, used by the step-2 cron).
//
// In v1.6 single-user mode the two paths see the same set of connections,
// but the gate distinguishes "user-initiated Ververs nu" from "system
// daily cron" for rate-limit + audit purposes.
//
// Wires the syncConnection orchestrator (from Phase 1.B) with real
// Directus + crypto + provider implementations.
//
// See docs/features/calendar-binding/step-1-google-oauth-and-context.md
// AC1.36-AC1.40.

import * as crypto from 'node:crypto';
import { NextResponse } from 'next/server';
import {
  createCalendarEvent,
  patchCalendarEvent,
  patchConnection,
  readActiveConnectionsForUser,
  readAllActiveConnections,
  readEventsByProviderIds,
  readSeriesExclusionRecurrenceIds,
} from '@/lib/api/calendars';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import { decrypt } from '@/lib/auth/envelope-encryption';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { parseSessionCookie } from '@/lib/auth/session';
import { calendarWriteRateLimiter, getClientIp } from '@/lib/auth/stores';
import { getGoogleProvider } from '@/lib/integrations/google/get-provider';
import {
  syncConnection,
  type SyncDeps,
  type SyncResult,
} from '@/lib/sync/calendar-sync';

function bearerMatches(authHeader: string | null, secret: string): boolean {
  if (!authHeader) return false;
  const m = /^Bearer\s+(.+)$/.exec(authHeader);
  if (!m || !m[1]) return false;
  const provided = Buffer.from(m[1]);
  const expected = Buffer.from(secret);
  if (provided.length !== expected.length) return false;
  try {
    return crypto.timingSafeEqual(provided, expected);
  } catch {
    return false;
  }
}

export async function POST(request: Request) {
  // ─────────────────────────────────────────────────────────────
  // Auth gate: bearer FIRST (cron path), then session (Ververs-nu path).
  // Bearer path uses process.env.DIRECTUS_TOKEN (TODO: step-2 will need
  // a different token — the scoped sessions-only token can't access
  // calendar collections. Defer to when the GHA cron actually fires).
  // Session path uses session.accessToken (user's per-request token,
  // tied to gevoelscore-frontend-api policy with calendar perms).
  // ─────────────────────────────────────────────────────────────
  const kek = process.env.CALENDAR_KEK;
  const syncSecret = process.env.CALENDAR_SYNC_SECRET;
  if (!kek) {
    return NextResponse.json({ error: 'server_error' }, { status: 500 });
  }

  let scope: 'session' | 'bearer';
  let accessToken: string;
  let userId: string | null = null;

  const authHeader = request.headers.get('authorization');
  if (authHeader && syncSecret && bearerMatches(authHeader, syncSecret)) {
    scope = 'bearer';
    // TODO(step-2): scoped sessions-only DIRECTUS_TOKEN can't access
    // calendar_connections. Need a separate "cron" token with the
    // gevoelscore-frontend-api policy (or a new admin-scope policy).
    const bearerToken = process.env.DIRECTUS_TOKEN;
    if (!bearerToken) {
      return NextResponse.json({ error: 'server_error' }, { status: 500 });
    }
    accessToken = bearerToken;
  } else {
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
    const willem = process.env.WILLEM_USER_ID;
    if (!willem) {
      return NextResponse.json({ error: 'server_error' }, { status: 500 });
    }
    userId = willem;
    accessToken = session.accessToken;

    const ip = getClientIp(request);
    const rl = calendarWriteRateLimiter.check(ip);
    if (!rl.allowed) {
      return NextResponse.json(
        { error: 'rate_limited', retry_after_ms: rl.retryAfterMs },
        { status: 429 },
      );
    }
    scope = 'session';
  }

  // ─────────────────────────────────────────────────────────────
  // Load active connections.
  // ─────────────────────────────────────────────────────────────
  const connectionsResult =
    scope === 'session'
      ? await readActiveConnectionsForUser(accessToken, userId!)
      : await readAllActiveConnections(accessToken);
  if (!connectionsResult.ok) {
    return NextResponse.json({ error: 'directus_error' }, { status: 502 });
  }
  const connections = connectionsResult.value;

  // ─────────────────────────────────────────────────────────────
  // Build orchestrator deps. Wraps the Result-shaped wrappers into
  // throw-on-error functions so syncConnection sees the same shape
  // its tests do.
  // ─────────────────────────────────────────────────────────────
  const deps: SyncDeps = {
    provider: getGoogleProvider(),
    decrypt: (enc) => decrypt(enc, kek),
    readSeriesExclusions: async (connId) => {
      const r = await readSeriesExclusionRecurrenceIds(accessToken, connId);
      if (!r.ok) throw new Error(r.error);
      return r.value;
    },
    readExistingEvents: async (connId, ids) => {
      const r = await readEventsByProviderIds(accessToken, connId, ids);
      if (!r.ok) throw new Error(r.error);
      return r.value;
    },
    createEvent: async (row) => {
      const r = await createCalendarEvent(accessToken, row);
      if (!r.ok) throw new Error(r.error);
    },
    updateEvent: async (id, patch) => {
      const r = await patchCalendarEvent(accessToken, id, patch);
      if (!r.ok) throw new Error(r.error);
    },
    updateConnection: async (id, patch) => {
      const r = await patchConnection(accessToken, id, patch);
      if (!r.ok) throw new Error(r.error);
    },
  };

  // ─────────────────────────────────────────────────────────────
  // Iterate connections sequentially (single-user app; sequential is
  // safe + simpler error semantics than Promise.all).
  // ─────────────────────────────────────────────────────────────
  const results: SyncResult[] = [];
  for (const connection of connections) {
    const result = await syncConnection(connection, deps, new Date());
    results.push(result);
  }

  return NextResponse.json(
    {
      ok: true,
      scope,
      connections: results.length,
      events_pulled: results.reduce((s, r) => s + r.eventsPulled, 0),
      events_upserted: results.reduce((s, r) => s + r.eventsUpserted, 0),
      events_excluded_by_series: results.reduce(
        (s, r) => s + r.eventsExcludedBySeries,
        0,
      ),
      errors: results.flatMap((r) => r.errors),
    },
    { status: 200 },
  );
}
