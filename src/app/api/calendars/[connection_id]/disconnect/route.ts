// POST /api/calendars/[connection_id]/disconnect
//
// Revokes the Google OAuth grant (best-effort) and deletes the local
// connection row. The FK CASCADE on calendar_events.connection_id +
// calendar_series_exclusions.connection_id removes the dependent rows
// automatically.
//
// Order: revoke FIRST so even if the local cascade fails, Google no
// longer has the grant. Revoke failure (other than the idempotent
// "already revoked") is logged in the response shape but does NOT
// prevent the local cascade.
//
// See docs/features/calendar-binding/step-1-google-oauth-and-context.md
// AC1.41-AC1.43.

import { NextResponse } from 'next/server';
import {
  deleteConnection,
  readConnectionById,
} from '@/lib/api/calendars';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import { decrypt } from '@/lib/auth/envelope-encryption';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { parseSessionCookie } from '@/lib/auth/session';
import { calendarWriteRateLimiter, getClientIp } from '@/lib/auth/stores';
import { isUuidShape } from '@/lib/domain/uuid';
import { getGoogleProvider } from '@/lib/integrations/google/get-provider';

type Context = { params: Promise<{ connection_id: string }> };

export async function POST(request: Request, context: Context) {
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
  const rl = calendarWriteRateLimiter.check(ip);
  if (!rl.allowed) {
    return NextResponse.json(
      { error: 'rate_limited', retry_after_ms: rl.retryAfterMs },
      { status: 429 },
    );
  }

  const userId = process.env.WILLEM_USER_ID;
  const adminToken = process.env.DIRECTUS_TOKEN;
  const kek = process.env.CALENDAR_KEK;
  if (!userId || !adminToken || !kek) {
    return NextResponse.json({ error: 'server_error' }, { status: 500 });
  }

  const { connection_id } = await context.params;
  if (!isUuidShape(connection_id)) {
    return NextResponse.json({ error: 'invalid_id' }, { status: 400 });
  }

  const connResult = await readConnectionById(adminToken, connection_id);
  if (!connResult.ok) {
    return NextResponse.json({ error: 'directus_error' }, { status: 502 });
  }
  if (!connResult.value) {
    return NextResponse.json({ error: 'not_found' }, { status: 404 });
  }
  if (connResult.value.user_id !== userId) {
    return NextResponse.json({ error: 'forbidden' }, { status: 403 });
  }
  const connection = connResult.value;

  // Revoke the Google grant. Best-effort: a failure here is captured in
  // the response but doesn't prevent the local cascade.
  let revokeOk = true;
  let revokeError: string | null = null;
  try {
    const refreshToken = decrypt(connection.refresh_token_encrypted, kek);
    const provider = getGoogleProvider();
    await provider.revoke(refreshToken);
  } catch (e) {
    revokeOk = false;
    revokeError =
      e instanceof Error ? e.message.slice(0, 100) : 'revoke_failed';
  }

  // Delete the local connection row. FK CASCADE removes events +
  // series_exclusions.
  const deleteResult = await deleteConnection(adminToken, connection_id);
  if (!deleteResult.ok) {
    return NextResponse.json(
      { error: 'directus_error', revoke_ok: revokeOk },
      { status: 502 },
    );
  }

  return NextResponse.json(
    {
      ok: true,
      revoke_ok: revokeOk,
      revoke_error: revokeError,
    },
    { status: 200 },
  );
}
