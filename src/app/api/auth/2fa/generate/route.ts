// POST /api/auth/2fa/generate
//
// Step 1 of 2FA setup: user re-enters their password, server asks Directus to
// generate a TOTP secret. Requires a valid gs_session cookie.

import { NextResponse } from 'next/server';
import { allowedOrigins } from '@/lib/auth/allowed-origins';
import { directusGenerateTfaSecret } from '@/lib/auth/directus-auth';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { PENDING_TFA_TTL_MS } from '@/lib/auth/pending-tfa';
import { parseSessionCookie } from '@/lib/auth/session';
import { getClientIp, pendingTfaStore, tfaGenerateRateLimiter } from '@/lib/auth/stores';

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
  const rl = tfaGenerateRateLimiter.check(ip);
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

  let body: { password?: unknown };
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
  }
  const password = typeof body.password === 'string' ? body.password : '';
  if (!password) {
    return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
  }

  const result = await directusGenerateTfaSecret(session.accessToken, password);
  if (!result.ok) {
    if (result.error === 'invalid_password') {
      return NextResponse.json({ error: 'invalid_password' }, { status: 401 });
    }
    if (result.error === 'invalid_token') {
      return NextResponse.json({ error: 'unauthenticated' }, { status: 401 });
    }
    // network_error, directus_error → generic
    return NextResponse.json({ error: 'server_error' }, { status: 502 });
  }

  // Bind the secret to the session so /enable can look it up without trusting
  // the client's posted value (audit H2).
  pendingTfaStore.create(sessionId, {
    secret: result.value.secret,
    expiresAt: Date.now() + PENDING_TFA_TTL_MS,
  });

  return NextResponse.json(
    { secret: result.value.secret, otpauth_url: result.value.otpauthUrl },
    { status: 200 },
  );
}
