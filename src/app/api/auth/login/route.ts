// POST /api/auth/login
//
// Composes the auth primitives from src/lib/auth/* into the public login
// endpoint. On success creates a session cookie. On accounts requiring 2FA,
// stashes the credentials server-side and returns { requires_otp: true } so
// the UI can navigate to /api/auth/login/verify.
//
// See docs/features/login/step-4-auth-route-handlers.md for AC mapping.

import { NextResponse } from 'next/server';
import { directusLogin } from '@/lib/auth/directus-auth';
import { validateOrigin } from '@/lib/auth/origin-check';
import { buildSessionCookie } from '@/lib/auth/session';
import { buildPendingOtpCookie } from '@/lib/auth/pending-otp';
import {
  getClientIp,
  loginRateLimiter,
  pendingOtpStore,
  sessionStore,
} from '@/lib/auth/stores';

const PENDING_OTP_TTL_MS = 5 * 60_000;
const PENDING_OTP_COOKIE_TTL_S = 300;
const SESSION_MAX_AGE_S = 60 * 60; // 1h, matches Directus access-token default

function allowedOrigins(): string[] {
  const origins: string[] = [];
  if (process.env.NEXT_PUBLIC_APP_URL) origins.push(process.env.NEXT_PUBLIC_APP_URL);
  if (process.env.NODE_ENV !== 'production') {
    origins.push('http://localhost:3000');
  }
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
  const rl = loginRateLimiter.check(ip);
  if (!rl.allowed) {
    return NextResponse.json(
      { error: 'rate_limited', retry_after_ms: rl.retryAfterMs },
      { status: 429 },
    );
  }

  let body: { email?: unknown; password?: unknown };
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
  }

  const email = typeof body.email === 'string' ? body.email.trim() : '';
  const password = typeof body.password === 'string' ? body.password : '';
  if (!email || !password || !email.includes('@')) {
    return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
  }

  const result = await directusLogin(email, password);

  if (!result.ok) {
    if (result.error === 'otp_required') {
      const pendingId = pendingOtpStore.create({
        email,
        password,
        expiresAt: Date.now() + PENDING_OTP_TTL_MS,
      });
      const res = NextResponse.json({ requires_otp: true }, { status: 200 });
      res.headers.append('Set-Cookie', buildPendingOtpCookie(pendingId, PENDING_OTP_COOKIE_TTL_S));
      return res;
    }
    // invalid_credentials, network_error, directus_error — all generic
    return NextResponse.json({ error: 'invalid_credentials' }, { status: 401 });
  }

  const sessionId = sessionStore.create({
    accessToken: result.value.accessToken,
    refreshToken: result.value.refreshToken,
    expiresAt: Date.now() + result.value.expiresInMs,
  });
  const res = NextResponse.json({ ok: true }, { status: 200 });
  res.headers.append('Set-Cookie', buildSessionCookie(sessionId, SESSION_MAX_AGE_S));
  return res;
}
