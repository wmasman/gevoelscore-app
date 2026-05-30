// POST /api/auth/login/verify
//
// Completes the 2FA login flow. Reads the gs_pending_otp cookie set by
// /api/auth/login when Directus required OTP, looks up the stashed
// credentials, and re-attempts login with the provided OTP. On success
// creates a session and clears the pending cookie.

import { NextResponse } from 'next/server';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import { directusLoginWithOtp } from '@/lib/auth/directus-auth';
import { validateOrigin } from '@/lib/auth/origin-check';
import { buildSessionCookie, SESSION_MAX_AGE_S } from '@/lib/auth/session';
import { buildPendingOtpCookie, parsePendingOtpCookie } from '@/lib/auth/pending-otp';
import { passesSingleUserGate } from '@/lib/auth/single-user-gate';
import {
  getClientIp,
  pendingOtpStore,
  sessionStore,
  verifyRateLimiter,
} from '@/lib/auth/stores';

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
  const rl = verifyRateLimiter.check(ip);
  if (!rl.allowed) {
    return NextResponse.json(
      { error: 'rate_limited', retry_after_ms: rl.retryAfterMs },
      { status: 429 },
    );
  }

  const pendingId = parsePendingOtpCookie(request.headers.get('cookie'));
  const pending = pendingId ? pendingOtpStore.get(pendingId) : undefined;
  if (!pending) {
    // AC10: no partial-state leaks — same generic error as a wrong code,
    // no hint about whether the cookie was missing vs. the code was wrong.
    return NextResponse.json({ error: 'invalid_otp' }, { status: 401 });
  }

  let body: { otp?: unknown };
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
  }
  const otp = typeof body.otp === 'string' ? body.otp.trim() : '';
  if (!otp) {
    return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
  }

  const result = await directusLoginWithOtp(pending.email, pending.password, otp);
  if (!result.ok) {
    // Per-pending-id attempt counter (audit M5). Three honest fumbles is the
    // realistic ceiling for a brainfog typo; beyond that we kill the pending
    // entry so the user must re-authenticate from /login.
    const OTP_ATTEMPT_CAP = 3;
    const attempts = pendingId ? pendingOtpStore.incrementAttempts(pendingId) ?? 0 : 0;
    if (attempts >= OTP_ATTEMPT_CAP) {
      if (pendingId) pendingOtpStore.delete(pendingId);
      const capped = NextResponse.json({ error: 'invalid_otp' }, { status: 401 });
      capped.headers.append('Set-Cookie', buildPendingOtpCookie(null, 0));
      return capped;
    }
    // AC7: invalid OTP → keep pending cookie so the user can retry (within rate limit + attempt cap)
    return NextResponse.json({ error: 'invalid_otp' }, { status: 401 });
  }

  // Single-user gate (S-H3 runtime enforcement). No-op when
  // WILLEM_USER_ID is unset (tests, dev).
  if (!(await passesSingleUserGate(result.value.accessToken, result.value.refreshToken))) {
    if (pendingId) pendingOtpStore.delete(pendingId);
    const denied = NextResponse.json({ error: 'invalid_otp' }, { status: 401 });
    denied.headers.append('Set-Cookie', buildPendingOtpCookie(null, 0));
    return denied;
  }

  // Success: create session, clear pending state + cookie
  const sessionId = await sessionStore.create({
    accessToken: result.value.accessToken,
    refreshToken: result.value.refreshToken,
    expiresAt: Date.now() + result.value.expiresInMs,
  });
  if (pendingId) pendingOtpStore.delete(pendingId);

  const res = NextResponse.json({ ok: true }, { status: 200 });
  res.headers.append('Set-Cookie', buildSessionCookie(sessionId, SESSION_MAX_AGE_S));
  res.headers.append('Set-Cookie', buildPendingOtpCookie(null, 0));
  return res;
}
