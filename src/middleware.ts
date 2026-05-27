// Next.js middleware — runs on every request matched by `config.matcher`.
// Edge runtime: only Edge-compatible imports allowed (string constants, no Node APIs).
//
// AC14 of the login feature: navigations to protected pages without a session
// cookie redirect to /login. Middleware is intentionally presence-only — it
// does NOT look up the cookie value in the server-side session store. That
// validation happens downstream (route handlers, page server components) when
// the session is actually used. This keeps middleware sub-millisecond.

import { NextResponse, type NextRequest } from 'next/server';
import { SESSION_COOKIE_NAME } from '@/lib/auth/session';

export function middleware(request: NextRequest) {
  const session = request.cookies.get(SESSION_COOKIE_NAME);
  if (!session?.value) {
    const loginUrl = new URL('/login', request.url);
    return NextResponse.redirect(loginUrl);
  }
  return NextResponse.next();
}

export const config = {
  // Run on every path EXCEPT the unauth surfaces:
  //   /login, /login/*           — login + verify UI (would loop otherwise)
  //   /api/auth/*                — auth endpoints handle their own auth flow
  //   /api/health                — Fly.io health check, no auth
  //   /_next/static, /_next/image — static assets
  //   /favicon.ico               — root favicon
  matcher: ['/((?!api/auth|api/health|_next/static|_next/image|favicon\\.ico|login).*)'],
};
