# Step 7: API-aware middleware (401 JSON instead of 307 redirect)

**Estimated time:** 20 minutes
**Test layer:** Playwright e2e (extends `tests/e2e/middleware.spec.ts`). The middleware is Edge runtime — Vitest's Node environment can't exercise it directly.
**Risk:** Low — pure branch in a 7-line file. Existing behaviour preserved for the page navigation case.
**Prerequisite:** Steps 1–6 done.

> Triggered by audit finding **M2**: today the middleware blanket-redirects unauthenticated requests to `/login`. For a browser navigation that's correct. For a future `fetch('/api/day-entries')` it returns an HTML redirect — the fetch client gets a 307 → 200 HTML body, not a 401 JSON, and the call silently appears to succeed. Daily-entry will land soon; if the middleware isn't API-aware before then, every protected fetch debugging session burns time.

---

## The problem

`src/middleware.ts`:

```ts
export function middleware(request: NextRequest) {
  const session = request.cookies.get(SESSION_COOKIE_NAME);
  if (!session?.value) {
    const loginUrl = new URL('/login', request.url);
    return NextResponse.redirect(loginUrl);
  }
  return NextResponse.next();
}
```

The matcher excludes `/api/auth/*` and `/api/health`. Any other `/api/*` path that lands later (the imminent `/api/day-entries`) flows through the middleware. Unauth → 307 redirect to `/login` → 200 HTML. A fetch client reading `await response.json()` against that gets a JSON parse error, not a `401`.

## Acceptance criteria

- [ ] AC1: An unauthenticated request whose pathname starts with `/api/` returns 401 with `{ error: 'unauthenticated' }` JSON.
- [ ] AC2: An unauthenticated browser navigation (any non-`/api/*` path) continues to receive a 307 redirect to `/login` (unchanged behaviour).
- [ ] AC3: An authenticated request (cookie present) on either path continues to `NextResponse.next()` (unchanged behaviour).

## Technical constraints

- Edge runtime: only Edge-compatible imports. No new ones needed.
- `pathname.startsWith('/api/')` check — the matcher already excludes the unauth-allowed `/api/auth/*` and `/api/health` surfaces, so any `/api/` path reaching the middleware is correctly protected.
- 401 vs 403: 401 is correct here — the client may be able to authenticate but has not yet (missing/invalid session). 403 would mean "authenticated but forbidden."

## Plan

### 7.1 Update `src/middleware.ts`

```ts
export function middleware(request: NextRequest) {
  const session = request.cookies.get(SESSION_COOKIE_NAME);
  if (!session?.value) {
    if (request.nextUrl.pathname.startsWith('/api/')) {
      return NextResponse.json({ error: 'unauthenticated' }, { status: 401 });
    }
    const loginUrl = new URL('/login', request.url);
    return NextResponse.redirect(loginUrl);
  }
  return NextResponse.next();
}
```

### 7.2 Extend `tests/e2e/middleware.spec.ts`

Add a case that hits any unmapped `/api/*` path (e.g. `/api/probe`) without a cookie and asserts a 401 JSON response, not an HTML redirect.

## Test plan

### `tests/e2e/middleware.spec.ts` (extended, +1 case)

- New case: "unauthenticated request to /api/probe returns 401 JSON (M2)" — uses `request.get('/api/probe')` (Playwright's bare HTTP client, no redirect-follow). Assert `response.status() === 401` and `response.json()` equals `{ error: 'unauthenticated' }`.

## Done criteria

- [x] `middleware.ts` carries the API-aware branch
- [x] New e2e case green; all 6 middleware specs pass against the dev server
- [x] `npm run verify` clean
- [x] Audit doc `M2` line marked `[Resolved 2026-05-27 — Step 7]`

### Side-quest caught during implementation

The first Playwright run returned 307 instead of 401 — a stale `node.exe` (PID 60616) was still bound to port 3000 from the Step 4 prod-build verification and Playwright's `reuseExistingServer: !CI` happily reused it. Killed the PID; the next run booted a fresh dev server with the new middleware. The behaviour is correct now but worth knowing: when iterating on middleware locally, kill stray dev servers before re-running e2e specs.
