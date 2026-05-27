// POST /api/auth/login/verify
//
// Completes the 2FA login flow. Reads the gs_pending_otp cookie set by
// /api/auth/login when Directus required OTP, looks up the stashed
// credentials, and re-attempts login with the provided OTP. On success
// creates a session and clears the pending cookie.

import { NextResponse } from 'next/server';
import { directusLoginWithOtp } from '@/lib/auth/directus-auth';
import { validateOrigin } from '@/lib/auth/origin-check';
import { buildSessionCookie } from '@/lib/auth/session';
import { buildPendingOtpCookie, parsePendingOtpCookie } from '@/lib/auth/pending-otp';
import {
  getClientIp,
  pendingOtpStore,
  sessionStore,
  verifyRateLimiter,
} from '@/lib/auth/stores';

const SESSION_MAX_AGE_S = 60 * 60;

function allowedOrigins(): string[] {
  const origins: string[] = [];
  if (process.env.NEXT_PUBLIC_APP_URL) origins.push(process.env.NEXT_PUBLIC_APP_URL);
  if (process.env.NODE_ENV !== 'production') origins.push('http://localhost:3000');
  return origins;
}

export async function POST(request: Request) {
  if (
    !validateOrigin(
      request.headers.get('origin'),
      request.headers.get('referer'),
      allowedOrigins(),
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
    // AC7: invalid OTP → keep pending cookie so the user can retry (within rate limit)
    return NextResponse.json({ error: 'invalid_otp' }, { status: 401 });
  }

  // Success: create session, clear pending state + cookie
  const sessionId = sessionStore.create({
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
