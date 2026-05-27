// POST /api/auth/2fa/generate
//
// Step 1 of 2FA setup: user re-enters their password, server asks Directus to
// generate a TOTP secret. Requires a valid gs_session cookie.

import { NextResponse } from 'next/server';
import { directusGenerateTfaSecret } from '@/lib/auth/directus-auth';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { parseSessionCookie } from '@/lib/auth/session';
import { getClientIp } from '@/lib/auth/stores';

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

  // ip kept for future rate-limiting / audit; ignored for now
  void getClientIp(request);

  const sessionId = parseSessionCookie(request.headers.get('cookie'));
  const session = sessionId ? await getValidatedSession(sessionId) : null;
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

  return NextResponse.json(
    { secret: result.value.secret, otpauth_url: result.value.otpauthUrl },
    { status: 200 },
  );
}
