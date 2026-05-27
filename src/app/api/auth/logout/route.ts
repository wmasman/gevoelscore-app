// POST /api/auth/logout
//
// Idempotent: returns 200 whether or not a valid session existed. Invalidates
// the Directus refresh token (best-effort — failure is treated as success
// because logout is allowed to be one-way), removes the server-side session
// entry, and clears the session cookie.

import { NextResponse } from 'next/server';
import { directusLogout } from '@/lib/auth/directus-auth';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { validateOrigin } from '@/lib/auth/origin-check';
import { buildSessionCookie, parseSessionCookie } from '@/lib/auth/session';
import { sessionStore } from '@/lib/auth/stores';

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

  const sessionId = parseSessionCookie(request.headers.get('cookie'));
  if (sessionId) {
    // getValidatedSession refreshes the token if needed so the subsequent
    // directusLogout call uses a live refresh token. If the session is
    // gone entirely (refresh failed), null is fine — logout is idempotent.
    const session = await getValidatedSession(sessionId);
    if (session) {
      await directusLogout(session.refreshToken);
      sessionStore.delete(sessionId);
    }
  }

  const res = NextResponse.json({ ok: true }, { status: 200 });
  res.headers.append('Set-Cookie', buildSessionCookie(null, 0));
  return res;
}
