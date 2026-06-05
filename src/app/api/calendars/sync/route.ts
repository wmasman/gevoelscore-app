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
  type CronRunResult,
  createCalendarEvent,
  patchCalendarEvent,
  patchConnection,
  readActiveConnectionsForUser,
  readAllActiveConnections,
  readEventsByProviderIds,
  readSeriesExclusionRecurrenceIds,
  recordCronRun,
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
  //
  // Bearer path uses CALENDAR_CRON_DIRECTUS_TOKEN — a scoped service
  // token tied to the `gevoelscore-frontend-api` policy (same policy
  // as session.accessToken, so CRUD on calendar_* + cron_monitor).
  // Provisioned by directus/scripts/setup-cron-service-token.mjs and
  // staged on Fly via scripts/rotate-cron-token.ps1. NOT the same as
  // the legacy `DIRECTUS_TOKEN` env var — that one is the
  // sessions-only scoped token (S-H1) and would FORBIDDEN on
  // calendar_connections.
  //
  // Session path uses session.accessToken (user's per-request token,
  // tied to the same gevoelscore-frontend-api policy).
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
    const bearerToken = process.env.CALENDAR_CRON_DIRECTUS_TOKEN;
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
  // Optional ?from=YYYY-MM-DD&to=YYYY-MM-DD window override (session
  // path only, for historical backfill). Bearer path keeps the
  // default 7-back/30-forward.
  // ─────────────────────────────────────────────────────────────
  let windowOverride: { from?: Date; to?: Date } | undefined;
  if (scope === 'session') {
    const requestUrl = new URL(request.url);
    const fromParam = requestUrl.searchParams.get('from');
    const toParam = requestUrl.searchParams.get('to');
    if (fromParam || toParam) {
      const override: { from?: Date; to?: Date } = {};
      if (fromParam) {
        const d = new Date(fromParam);
        if (Number.isNaN(d.getTime())) {
          return NextResponse.json(
            { error: 'invalid_from' },
            { status: 400 },
          );
        }
        override.from = d;
      }
      if (toParam) {
        const d = new Date(toParam);
        if (Number.isNaN(d.getTime())) {
          return NextResponse.json({ error: 'invalid_to' }, { status: 400 });
        }
        override.to = d;
      }
      windowOverride = override;
    }
  }

  // ─────────────────────────────────────────────────────────────
  // Iterate connections sequentially (single-user app; sequential is
  // safe + simpler error semantics than Promise.all).
  // ─────────────────────────────────────────────────────────────
  const results: SyncResult[] = [];
  for (const connection of connections) {
    const result = await syncConnection(connection, deps, new Date(), windowOverride);
    results.push(result);
  }

  const eventsPulled = results.reduce((s, r) => s + r.eventsPulled, 0);
  const eventsUpserted = results.reduce((s, r) => s + r.eventsUpserted, 0);
  const eventsExcludedBySeries = results.reduce(
    (s, r) => s + r.eventsExcludedBySeries,
    0,
  );
  const errors = results.flatMap((r) => r.errors);

  // ─────────────────────────────────────────────────────────────
  // cron_monitor write (step-2 Phase 2.B, AC2.3/2.4/2.5).
  //
  // Called on BOTH paths (manual Ververs nu AND daily cron) so the
  // monitor row is "last sync, however triggered" — the most useful
  // signal for staleness checks. Result body is counts-only on success
  // (AC2.2) and a short error code on failure (AC2.3); the wrapper
  // enforces a 1000-char cap as a final defense.
  //
  // recordCronRun is no-throw by contract (AC2.5), but the .catch()
  // here is defense in depth: a future bug in the wrapper cannot
  // break Ververs nu's 200 response or the cron's HTTP signal.
  // ─────────────────────────────────────────────────────────────
  const cronResult: CronRunResult =
    errors.length === 0
      ? {
          ok: true,
          details: {
            connections: results.length,
            events_pulled: eventsPulled,
            events_upserted: eventsUpserted,
            events_excluded_by_series: eventsExcludedBySeries,
          },
        }
      : { ok: false, error: errors[0]! };
  await recordCronRun(accessToken, 'daily_calendar_sync', cronResult).catch(
    () => undefined,
  );

  return NextResponse.json(
    {
      ok: true,
      scope,
      connections: results.length,
      events_pulled: eventsPulled,
      events_upserted: eventsUpserted,
      events_excluded_by_series: eventsExcludedBySeries,
      errors,
    },
    { status: 200 },
  );
}
