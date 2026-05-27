# Step 2: Rate limiter + session map (server-side primitives)

**Estimated time:** 1–2 hours
**Test layer:** Domain (pure logic, Vitest, no platform deps)
**Risk:** Low — both modules are isolated in-memory state. No network, no DB, no React.
**Prerequisite:** Step 1 (Next.js bootstrap) — done 2026-05-27

> TDD is mandatory — see [`.claude/testing.md`](../../../.claude/testing.md).
> This is the first deliverable inside the auth library. Higher-level steps (login flow, TOTP flow, route handlers, UI) compose these primitives.

---

## Acceptance criteria (subset of the feature README's 18 ACs)

- [ ] AC5: A login endpoint can ask the rate limiter "has this IP been blocked?" and gets a yes/no within ~µs. Block window: 5 attempts per 5 minutes per key. The 6th attempt returns "blocked" until the window expires.
- [ ] AC8: Same shape, used by the TOTP-verify endpoint — different key namespace so login and verify rate-limits don't share a counter.
- [ ] AC11 (partial): The session module exposes cookie-helper functions that produce a cookie string with `httpOnly`, `Secure`, `SameSite=Strict`, `Path=/`, `Max-Age=<seconds>`. The actual cookie-setting happens at the route-handler layer (Step 5); this step delivers the primitives.
- [ ] AC12 (partial): The session module manages a `Map<sessionId, { accessToken, refreshToken, expiresAt }>` keyed by a random UUID. `createSession`, `getSession`, `deleteSession`, `cleanupExpired`. Browser JS never touches the access token — that's enforced upstream by the route-handler layer; this step delivers the server-side store.
- [ ] AC13 (partial): The `deleteSession` primitive that the logout route will call.

What this step does NOT cover (deferred to later steps):
- The actual rate-limit *enforcement* in a route handler (Step 5)
- The Directus client / token refresh logic (Step 4)
- The middleware that reads cookies and redirects (Step 7)
- Origin check (Step 3)

## Technical constraints (this step)

- [ ] Pure TS, zero platform deps — no `next/*`, no `@directus/sdk`, no React. Both modules must be importable from any Node context (Route Handler, server component, unit test).
- [ ] No I/O in either module (no fs, no fetch, no DB).
- [ ] In-memory only. Single-process Fly machine (`min_machines_running = 1` per ADR 0003) makes this fine; if scaled later, swap to Redis or a Directus collection — same API.
- [ ] Time-based logic uses an injectable `now()` function (default `Date.now`) so tests are deterministic without `vi.setSystemTime`.
- [ ] Session IDs are UUIDs from `crypto.randomUUID()` (Web Crypto API, built-in to Node 18+). No `uuid` package.
- [ ] No PII in logs — rate-limit module logs hit-counts but never the key (key is "an IP" externally, but treat it as opaque inside the module).
- [ ] Functions over classes where the API is simple.

## Test plan

Two new test files. Both pure Vitest.

### File 1: `src/lib/auth/__tests__/rate-limit.test.ts`

```typescript
import { describe, expect, it } from 'vitest';
import { createRateLimiter } from '../rate-limit';

describe('rate-limit', () => {
  describe('createRateLimiter', () => {
    it('allows attempts up to the limit, then blocks the next one', () => {
      let now = 1_000_000;
      const limiter = createRateLimiter({
        limit: 5,
        windowMs: 5 * 60_000,
        now: () => now,
      });

      // 5 attempts — all allowed
      for (let i = 0; i < 5; i++) {
        const r = limiter.check('203.0.113.1');
        expect(r.allowed).toBe(true);
        expect(r.remaining).toBe(4 - i);
      }

      // 6th — blocked
      const blocked = limiter.check('203.0.113.1');
      expect(blocked.allowed).toBe(false);
      expect(blocked.retryAfterMs).toBeGreaterThan(0);
    });

    it('resets the counter after the window expires', () => {
      let now = 1_000_000;
      const limiter = createRateLimiter({
        limit: 5,
        windowMs: 5 * 60_000,
        now: () => now,
      });

      for (let i = 0; i < 5; i++) limiter.check('1.2.3.4');
      expect(limiter.check('1.2.3.4').allowed).toBe(false);

      // Advance past the window
      now += 5 * 60_000 + 1;
      const fresh = limiter.check('1.2.3.4');
      expect(fresh.allowed).toBe(true);
      expect(fresh.remaining).toBe(4);
    });

    it('isolates keys — one IP being blocked does not affect another', () => {
      const limiter = createRateLimiter({ limit: 5, windowMs: 60_000 });

      for (let i = 0; i < 5; i++) limiter.check('1.1.1.1');
      expect(limiter.check('1.1.1.1').allowed).toBe(false);
      expect(limiter.check('2.2.2.2').allowed).toBe(true);
    });

    it('isolates namespaces — login and totp counters do not share', () => {
      const loginLimiter = createRateLimiter({ limit: 5, windowMs: 60_000 });
      const totpLimiter = createRateLimiter({ limit: 5, windowMs: 60_000 });

      for (let i = 0; i < 5; i++) loginLimiter.check('9.9.9.9');
      expect(loginLimiter.check('9.9.9.9').allowed).toBe(false);
      expect(totpLimiter.check('9.9.9.9').allowed).toBe(true);
    });

    it('cleans up expired entries when sweep() is called', () => {
      let now = 1_000_000;
      const limiter = createRateLimiter({
        limit: 5,
        windowMs: 60_000,
        now: () => now,
      });

      limiter.check('1.1.1.1');
      limiter.check('2.2.2.2');
      expect(limiter.size()).toBe(2);

      now += 60_000 + 1;
      limiter.sweep();
      expect(limiter.size()).toBe(0);
    });

    it('reports retryAfterMs as the remaining window time, not the full window', () => {
      let now = 1_000_000;
      const limiter = createRateLimiter({
        limit: 5,
        windowMs: 60_000,
        now: () => now,
      });

      for (let i = 0; i < 5; i++) limiter.check('1.1.1.1');
      now += 20_000; // 20s into the window
      const blocked = limiter.check('1.1.1.1');

      expect(blocked.allowed).toBe(false);
      expect(blocked.retryAfterMs).toBeGreaterThan(0);
      expect(blocked.retryAfterMs).toBeLessThanOrEqual(40_000);
    });
  });
});
```

### File 2: `src/lib/auth/__tests__/session.test.ts`

```typescript
import { describe, expect, it } from 'vitest';
import {
  createSessionStore,
  buildSessionCookie,
  parseSessionCookie,
  SESSION_COOKIE_NAME,
} from '../session';

describe('session', () => {
  describe('createSessionStore', () => {
    it('creates a session and returns an opaque session id', () => {
      const store = createSessionStore();

      const id = store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: Date.now() + 60_000,
      });

      expect(typeof id).toBe('string');
      expect(id.length).toBeGreaterThan(20); // crypto.randomUUID is 36 chars
    });

    it('returns the session by id', () => {
      const store = createSessionStore();
      const id = store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: Date.now() + 60_000,
      });

      const session = store.get(id);
      expect(session?.accessToken).toBe('at-1');
      expect(session?.refreshToken).toBe('rt-1');
    });

    it('returns undefined for an unknown id', () => {
      const store = createSessionStore();
      expect(store.get('does-not-exist')).toBeUndefined();
    });

    it('returns undefined for an expired session and removes it', () => {
      let now = 1_000_000;
      const store = createSessionStore({ now: () => now });
      const id = store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: now + 1_000,
      });

      now += 2_000;
      expect(store.get(id)).toBeUndefined();
      expect(store.size()).toBe(0);
    });

    it('delete removes the session', () => {
      const store = createSessionStore();
      const id = store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: Date.now() + 60_000,
      });

      store.delete(id);
      expect(store.get(id)).toBeUndefined();
    });

    it('cleanupExpired removes only expired sessions', () => {
      let now = 1_000_000;
      const store = createSessionStore({ now: () => now });

      const liveId = store.create({
        accessToken: 'live',
        refreshToken: 'rt-live',
        expiresAt: now + 60_000,
      });
      store.create({
        accessToken: 'expired',
        refreshToken: 'rt-expired',
        expiresAt: now - 1,
      });

      store.cleanupExpired();
      expect(store.size()).toBe(1);
      expect(store.get(liveId)).toBeDefined();
    });

    it('uses an injected idGenerator when provided (deterministic tests)', () => {
      let counter = 0;
      const store = createSessionStore({
        idGenerator: () => `id-${++counter}`,
      });

      const id = store.create({
        accessToken: 'at',
        refreshToken: 'rt',
        expiresAt: Date.now() + 60_000,
      });
      expect(id).toBe('id-1');
    });
  });

  describe('buildSessionCookie', () => {
    it('produces a httpOnly Secure SameSite=Strict cookie with Max-Age', () => {
      const cookie = buildSessionCookie('abc-123', 3600);

      expect(cookie).toContain(`${SESSION_COOKIE_NAME}=abc-123`);
      expect(cookie).toContain('HttpOnly');
      expect(cookie).toContain('Secure');
      expect(cookie).toContain('SameSite=Strict');
      expect(cookie).toContain('Path=/');
      expect(cookie).toContain('Max-Age=3600');
    });

    it('produces a cookie deletion string when sessionId is null', () => {
      const cookie = buildSessionCookie(null, 0);

      expect(cookie).toContain(`${SESSION_COOKIE_NAME}=`);
      expect(cookie).toContain('Max-Age=0');
      expect(cookie).toContain('HttpOnly');
      expect(cookie).toContain('Secure');
    });
  });

  describe('parseSessionCookie', () => {
    it('extracts the session id from a Cookie header', () => {
      const header = `${SESSION_COOKIE_NAME}=abc-123; other=foo`;
      expect(parseSessionCookie(header)).toBe('abc-123');
    });

    it('returns null when the cookie is absent', () => {
      expect(parseSessionCookie('other=foo; another=bar')).toBeNull();
    });

    it('returns null for an empty or null header', () => {
      expect(parseSessionCookie('')).toBeNull();
      expect(parseSessionCookie(null)).toBeNull();
    });
  });
});
```

---

## Done criteria

- [ ] Both test files exist and fail BEFORE implementation (RED captured)
- [ ] `src/lib/auth/rate-limit.ts` exists and tests pass (GREEN captured)
- [ ] `src/lib/auth/session.ts` exists and tests pass (GREEN captured)
- [ ] Full Vitest suite still passes (254 existing + new) with zero regressions
- [ ] `npm run typecheck` clean
- [ ] `npm run lint` clean
- [ ] No new HIGH gate findings (no telemetry deps, no PII logged, no `localStorage` use)
- [ ] No walkthrough needed (no UI changed)
- [ ] Refactor pass complete (or "none needed")

---

## Execution order (followed by `/build-step`)

### 2.1 Baseline

No baseline — these are new modules. Skip.

### 2.2 Write tests (RED)

Paste both test files above. Run:

```
npm test -- rate-limit session
```

Must FAIL with "Cannot find module '../rate-limit'" and "Cannot find module '../session'".

### 2.3 Implement (GREEN)

Smallest code that turns RED tests GREEN.

Files to create:
- `src/lib/auth/rate-limit.ts` — `createRateLimiter(config) → { check(key), sweep(), size() }`
- `src/lib/auth/session.ts` — `createSessionStore(config?) → { create(data), get(id), delete(id), cleanupExpired(), size() }`, plus `buildSessionCookie`, `parseSessionCookie`, `SESSION_COOKIE_NAME` exports

Reference patterns from:
- [src/lib/domain/score.ts](../../../src/lib/domain/score.ts) — Result-style return shape (`{ ok: true, ... } | { ok: false, ... }`)
- The auth README's "Technical constraints" section — in-memory store rationale

Run again:

```
npm test -- rate-limit session
```

Must PASS.

### 2.4 Regression check

```
npm test
```

Existing 254 tests + new (~13 from rate-limit, ~10 from session) all pass.

### 2.5 Refactor

Clean up while GREEN stays GREEN. Likely candidates:
- Shared helper for "purge entries older than now" between the two modules (only if both turn out to need exactly the same shape)
- JSDoc on the public functions (keep terse)

### 2.6 No walkthrough

Step doesn't touch the daily screen. Skip.

### 2.7 Checkpoint

Commit when GREEN and clean:

```
feat(auth): rate-limit + session-map primitives

Step 2 of the login feature (docs/features/login). Two pure-TS in-memory
state stores, both injectable-clock for deterministic tests:

- rate-limit.ts: 5 attempts / 5 min window per key, per limiter instance
  (separate namespaces for login and totp). Block returns retryAfterMs.
- session.ts: createSessionStore + buildSessionCookie + parseSessionCookie
  + SESSION_COOKIE_NAME. Cookie attrs: httpOnly Secure SameSite=Strict Path=/.

Tests: vitest, ~23 new cases, all 277 still green. Higher-level auth flow
(Step 3 origin-check, Step 4 login/totp orchestrator, Step 5 route handlers,
Step 6 /login UI) compose these primitives.
```

---

## What this step does NOT do

- **No Route Handler.** The rate limiter and session store are libraries. Mounting them on `/api/auth/*` is Step 5.
- **No Directus client.** Step 4.
- **No cookie *setting*** — `buildSessionCookie` returns the string. The route handler will pass it to `Response.headers.append('Set-Cookie', ...)`. Step 5.
- **No origin / CSRF check.** Step 3.
- **No Playwright tests.** These modules have no I/O, no route, no UI. Unit tests are the right layer. Playwright will exercise them indirectly when Step 5's API tests run.
- **No persistence.** In-memory only. If multi-machine scaling is ever needed, the API stays the same — only the storage layer changes.
