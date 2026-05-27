# Step 4: Security response headers

**Estimated time:** 45 minutes
**Test layer:** Playwright live-stack spec (asserts headers against the production build) — the dev server's behaviour differs, so Vitest cannot meaningfully cover this.
**Risk:** Low. CSP is the one that can break things if Next's hydration uses an unexpected source — but the app today has zero third-party origins, so `default-src 'self'` is safe with `'unsafe-inline'` permitted on `script-src` (Next inlines its hydration bootstrap as inline `<script>`).
**Prerequisite:** Steps 1–3 done.

> Triggered by audit finding **M1**: zero security headers in production. `curl -I https://gevoelscore-frontend.fly.dev/login` returns no CSP, no HSTS, no Referrer-Policy, no Permissions-Policy, no X-Content-Type-Options — and reflects `X-Powered-By: Next.js`.

---

## The problem

The audit explicitly verified this gap live: `curl -I https://gevoelscore-frontend.fly.dev/login` post-deploy showed none of the five headers the project's own [`.claude/security-checklist.md`](../../../.claude/security-checklist.md) A05 mandates. Next.js does not set them by default — they have to be declared in `next.config.ts`.

Each header is a small but meaningful defense:

- **CSP** `default-src 'self'`: any future XSS that smuggles in a `<script src="evil.example.com">` becomes a no-op.
- **HSTS**: forces TLS for a year. Strengthens what `force_https = true` already does at the Fly edge layer.
- **X-Content-Type-Options: nosniff**: stops the browser from guessing a MIME type and executing a misclassified response.
- **Referrer-Policy: strict-origin-when-cross-origin**: standard hygiene; we don't leak the path on cross-origin links.
- **Permissions-Policy**: explicitly deny camera/microphone/geolocation. None of the v1 app needs them; future features should opt in via PR rather than be silently granted.

## Acceptance criteria

Maps to [README](README.md) AC11–AC14:

- [ ] AC11: Production-build responses carry `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` (camera/microphone/geolocation = ()).
- [ ] AC12: `X-Powered-By` is not reflected (set `poweredByHeader: false`).
- [ ] AC13: CSP `default-src 'self'`; `script-src 'self' 'unsafe-inline'` (Next inlines hydration bootstrap script tags); `style-src 'self' 'unsafe-inline'` (Tailwind inlines runtime CSS in some flows); `img-src 'self' data:`; `connect-src 'self'`; `frame-ancestors 'none'`; `base-uri 'self'`; `form-action 'self'`.
- [ ] AC14: New Playwright live-stack spec `tests/live-stack/security-headers.spec.ts` asserts all five headers (+ absence of `X-Powered-By`) on `/login` and `/api/health`.

## Technical constraints

- All headers via `async headers()` in `next.config.ts`. Single source of truth.
- HSTS: `max-age=31536000; includeSubDomains` — one year, including subdomains. No `preload` until the domain is explicitly added to the HSTS preload list.
- CSP: report-only NOT used; the goal is enforcement. Mistakes show up immediately in dev and live-stack tests rather than silently in browser console.
- The check runs against `npm run build && npm run start` via the existing live-stack Playwright config — dev-mode Next adds development-only sources to CSP that would make the test brittle.

## Plan

### 4.1 `next.config.ts`

```ts
import type { NextConfig } from 'next';

const SECURITY_HEADERS = [
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline'",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data:",
      "connect-src 'self'",
      "frame-ancestors 'none'",
      "base-uri 'self'",
      "form-action 'self'",
    ].join('; '),
  },
  { key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  {
    key: 'Permissions-Policy',
    value: 'camera=(), microphone=(), geolocation=()',
  },
];

const config: NextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  poweredByHeader: false,
  async headers() {
    return [{ source: '/:path*', headers: SECURITY_HEADERS }];
  },
};

export default config;
```

### 4.2 New Playwright live-stack spec

`tests/live-stack/security-headers.spec.ts`:

```ts
import { test, expect } from '@playwright/test';

const REQUIRED = [
  'content-security-policy',
  'strict-transport-security',
  'x-content-type-options',
  'referrer-policy',
  'permissions-policy',
];

test('all five security headers present on /login (M1 fix)', async ({ request }) => {
  const res = await request.get('/login');
  for (const h of REQUIRED) {
    expect(res.headers()[h], `missing header: ${h}`).toBeDefined();
  }
  expect(res.headers()['x-powered-by']).toBeUndefined();
});

test('all five security headers present on /api/health', async ({ request }) => {
  const res = await request.get('/api/health');
  for (const h of REQUIRED) {
    expect(res.headers()[h]).toBeDefined();
  }
});

test('CSP locks default-src to self, denies frame-ancestors', async ({ request }) => {
  const res = await request.get('/login');
  const csp = res.headers()['content-security-policy'] ?? '';
  expect(csp).toContain("default-src 'self'");
  expect(csp).toContain("frame-ancestors 'none'");
});
```

### 4.3 Deploy verification

After landing: `curl -I https://gevoelscore-frontend.fly.dev/login`. Capture in this step's Done section.

## Done criteria

- [x] `next.config.ts` carries the 5 headers + `poweredByHeader: false`
- [x] New live-stack spec `tests/live-stack/security-headers.spec.ts` passes against `npm run build && npm run start` — 5/5 local prod-build green
- [x] No regressions in any existing Vitest spec (369/369 green)
- [x] `npm run lint` + `npm run typecheck` clean
- [x] Local `curl -I http://localhost:3000/login` confirmed all 5 headers + no `X-Powered-By` (see evidence below)
- [x] Live `curl -I https://gevoelscore-frontend.fly.dev/login` after Fly deploy: all 5 headers present, no `X-Powered-By`
- [x] Audit doc `M1` line marked `[Resolved 2026-05-27]`

### Evidence — local prod build curl

```
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

No `X-Powered-By` line in output → `poweredByHeader: false` working.

### Playwright result

```
5 passed (637ms)
  ok 1 — all five security headers present on /login
  ok 2 — all five security headers present on /api/health
  ok 3 — CSP locks default-src to self and denies framing
  ok 4 — HSTS asserts a long max-age and includeSubDomains
  ok 5 — X-Content-Type-Options is nosniff
```

## What this step does NOT do

- Does not configure CSP reporting (`report-uri` / `report-to`). The app has no log-collection endpoint and adding one would introduce telemetry — explicit no per ADR 0002.
- Does not add HSTS preload (`preload` directive + submission to hstspreload.org). Adding `preload` is a one-way door — requires a separate review.
- Does not set `Cross-Origin-Opener-Policy` / `Cross-Origin-Embedder-Policy`. The app has no embedded iframes or SharedArrayBuffer usage; these would be churn for no current benefit. Revisit if a service worker / push API lands.
