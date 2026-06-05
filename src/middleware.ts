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
    // API requests get a parseable 401 JSON; browser navigations get the
    // /login redirect. Audit M2 — fetch clients should not have to parse
    // an HTML redirect to learn they're unauthenticated.
    if (request.nextUrl.pathname.startsWith('/api/')) {
      return NextResponse.json({ error: 'unauthenticated' }, { status: 401 });
    }
    const loginUrl = new URL('/login', request.url);
    return NextResponse.redirect(loginUrl);
  }
  return NextResponse.next();
}

export const config = {
  // Run on every path EXCEPT the unauth surfaces:
  //   /login, /login/*           — login + verify UI (would loop otherwise)
  //   /over, /over/*             — public landing / backer-recruitment page
  //   /api/auth/*                — auth endpoints handle their own auth flow
  //   /api/health                — Fly.io health check, no auth (matches
  //                                /api/health AND /api/health/cron via prefix)
  //   /api/calendars/sync        — bearer-gated cron endpoint (step-2). Auth
  //                                lives in the route handler (constant-time
  //                                compare against CALENDAR_SYNC_SECRET). The
  //                                middleware presence-check would 401 the
  //                                cron's cookieless POST before the route
  //                                ran, which is exactly what bit step-2's
  //                                smoke until this exclusion landed.
  //   /_next/static, /_next/image — static assets
  //   /favicon.ico               — root favicon
  //   any path ending in .ext    — public static assets like
  //                                /manifest.webmanifest, future /sw.js,
  //                                icons, etc. Without this, the PWA
  //                                manifest gets 307-redirected to /login
  //                                for unauthenticated visitors and the
  //                                browser tries to parse HTML as JSON
  //                                (Manifest: Line 1, column 1, Syntax error).
  //                                Our API routes have no dots in their
  //                                paths, so this is safe.
  matcher: ['/((?!api/auth|api/health|api/calendars/sync|_next/static|_next/image|favicon\\.ico|login|over|.*\\.[a-zA-Z0-9]+$).*)'],
};
