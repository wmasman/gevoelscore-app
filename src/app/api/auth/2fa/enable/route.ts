// POST /api/auth/2fa/enable
//
// Step 2 of 2FA setup: user has added the secret to their authenticator and
// enters the 6-digit code. Server confirms with Directus, which activates
// 2FA on the account.

import { NextResponse } from 'next/server';
import { directusEnableTfa } from '@/lib/auth/directus-auth';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { parseSessionCookie } from '@/lib/auth/session';
import { getClientIp, pendingTfaStore, tfaEnableRateLimiter } from '@/lib/auth/stores';

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
  const rl = tfaEnableRateLimiter.check(ip);
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

  // Server-side binding: look up the secret stashed by /2fa/generate. Ignore
  // any `secret` field on the body (audit H2).
  const pending = pendingTfaStore.get(sessionId);
  if (!pending) {
    return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
  }

  const result = await directusEnableTfa(session.accessToken, pending.secret, otp);
  if (!result.ok) {
    if (result.error === 'invalid_otp') {
      return NextResponse.json({ error: 'invalid_otp' }, { status: 401 });
    }
    if (result.error === 'invalid_token') {
      return NextResponse.json({ error: 'unauthenticated' }, { status: 401 });
    }
    return NextResponse.json({ error: 'server_error' }, { status: 502 });
  }

  pendingTfaStore.delete(sessionId);
  return NextResponse.json({ ok: true }, { status: 200 });
}
