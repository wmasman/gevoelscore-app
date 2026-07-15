# Frontend setup

Concrete shape of the Next.js frontend in this repo: dependencies, configs, test layers, and how the pieces fit. The "why" lives in [ADR 0002](../decisions/0002-pwa-with-directus-backend.md) (stack choice) and [ADR 0003](../decisions/0003-directus-fly-infra-setup.md) (deploy shape). This doc is the operational reference for "what's actually wired up."

**Bootstrapped 2026-05-27**, commit `45e356b`. Single-repo layout (not a `/frontend` sub-folder) — `src/app/` for routes, `src/lib/` shared with the existing pure-TS domain layer.

---

## Dependencies

From [package.json](../../package.json):

| Package | Version | Why |
|---|---|---|
| `next` | ^15.1 | App Router, Route Handlers, standalone output for Docker |
| `react`, `react-dom` | ^19.0 | Required peer for Next 15 |
| `@directus/sdk` | ^18.0 | Frontend Directus client — matches programmeerprobeer's version. See "SDK choice" below. |
| `tailwindcss`, `@tailwindcss/postcss`, `postcss` | ^4.0 / ^4.0 / ^8.4 | Utility CSS, v4's CSS-first config (no `tailwind.config.js` for basic usage) |
| `eslint`, `eslint-config-next`, `@eslint/eslintrc` | ^9.0 / ^15.1 / ^3.0 | Flat config with `next/core-web-vitals` + `next/typescript` |
| `@playwright/test` | ^1.49 | Closed-loop API + e2e testing layer |
| `typescript`, `vitest`, `@types/node`, `@types/react`, `@types/react-dom` | dev | Unit testing + types |

Pinned to Tailwind v4 (CSS-first, no `tailwind.config.js` for basic use). PostCSS plugin is `@tailwindcss/postcss` (replaces the v3 `tailwindcss` + `postcss-import` + `autoprefixer` trio).

---

## File layout

```
gevoelscore-app/
├── Dockerfile                — Multi-stage with `next standalone` output (~50MB runtime image)
├── fly.toml                  — Fly app config for gevoelscore-frontend (ams, 512MB, /api/health check)
├── .dockerignore             — Excludes directus/, docs/, private/, tests/
├── next.config.ts            — output: 'standalone', reactStrictMode: true, no telemetry
├── postcss.config.mjs        — @tailwindcss/postcss only
├── eslint.config.mjs         — Flat config; ignores .next/, node_modules/, directus/, next-env.d.ts
├── playwright.config.ts      — Two projects (api, chromium); auto-starts `next dev`
├── tsconfig.json             — strict + noUncheckedIndexedAccess; @/* → src/*
├── vitest.config.ts          — Resolves @/* path alias for route-handler tests
├── src/
│   ├── app/
│   │   ├── layout.tsx        — html lang="nl", Metadata + Viewport
│   │   ├── page.tsx          — Minimal home shell (placeholder for daily-entry)
│   │   ├── globals.css       — @import "tailwindcss" + minimal base
│   │   └── api/
│   │       ├── health/route.ts                    — GET, static, no auth (fly.toml health check)
│   │       └── auth/
│   │           ├── login/route.ts                 — POST: email+password → cookie or otp-required
│   │           ├── login/verify/route.ts          — POST: otp → cookie
│   │           └── logout/route.ts                — POST: idempotent
│   └── lib/
│       ├── domain/           — Pure TS validators (unchanged from pre-bootstrap)
│       ├── import/           — CSV parser (unchanged)
│       └── auth/             — rate-limit, session, pending-otp, origin-check, directus-auth, stores
└── tests/
    ├── api/                  — Playwright `request` fixture against real HTTP
    │   ├── health.spec.ts
    │   └── auth/             — login.spec.ts, login-verify.spec.ts, logout.spec.ts
    └── e2e/                  — Playwright browser
        └── home.spec.ts
```

---

## Test layers (the closed loop)

Three layers, all required for any route or screen change. See [`.claude/testing.md`](../../.claude/testing.md) for the full doctrine.

| Layer | Runner | Lives in | Hits | Use for |
|---|---|---|---|---|
| Unit | Vitest (Node) | `src/lib/**/__tests__/` | Pure TS, mocked deps | Domain logic, auth library modules |
| Route handler | Vitest (Node) | `src/app/api/**/__tests__/` | `POST(request)` directly; stores + SDK mocked via `vi.mock` | Cookie attrs, full happy paths, status codes |
| API integration | Playwright `request` fixture | `tests/api/` | Real HTTP against `next dev` | Validation, origin check, idempotency, wiring |
| e2e | Playwright Chromium | `tests/e2e/` | Real browser, real navigation | Form behavior, redirects, visual baseline |

**One Playwright config** ([playwright.config.ts](../../playwright.config.ts)) covers both API and e2e via two `projects`. `webServer` auto-starts `npm run dev` and sets `DIRECTUS_URL=127.0.0.1:65535` so unhappy-path tests can't accidentally hit production Directus.

**`@/*` path alias** is resolved in three places: [tsconfig.json](../../tsconfig.json) (compiler), Next.js (built-in `paths` support), and [vitest.config.ts](../../vitest.config.ts) (manual `resolve.alias`). Forgetting the vitest one was the first bug caught during route-handler tests.

**Module-state caveat for Playwright API tests**: `next dev` re-evaluates server modules between requests, which resets in-memory state (rate limiter, session map). The Vitest route-handler tests cover happy paths against mocked stores; the Playwright API specs cover unhappy paths where state doesn't need to persist. Tests that depend on persistent state (rate-limit enforcement end-to-end) are deferred to **Step 7 of the login feature** which runs against `next start` / live Fly stack.

**Commands:**

```powershell
npm test           # Vitest, all unit + route-handler tests
npm run test:e2e   # Playwright, both projects (api + chromium)
npm run test:all   # Vitest then Playwright
npm run typecheck  # tsc --noEmit
npm run lint       # eslint with flat config
npm run dev        # Next dev server (used by Playwright webServer)
npm run build      # Next standalone build (for Docker / Fly)
```

---

## SDK choice: `@directus/sdk` v18

The frontend uses the official Directus SDK; the [`directus/scripts/`](../../directus/scripts/) folder continues to use plain `fetch` (different audience: dep-free batch scripts).

Reason for the split:

- **Frontend (SDK)** — many Directus interactions are coming (`day_entries` with M2M `tags`, `projects`, `calendar_events`). The SDK pays off through typed queries (`readItems('day_entries', { fields: ['*', 'tags.tags_id.label'] })`), built-in token refresh, and matching programmeerprobeer's frontend pattern.
- **Scripts (plain fetch)** — `directus/` has no `node_modules`. Scripts are one-shot batch operations; field expansion isn't useful; zero deps is a hard requirement.

The auth library wraps the SDK behind Result-style functions in [`src/lib/auth/directus-auth.ts`](../../src/lib/auth/directus-auth.ts) — every call creates a fresh SDK client (no shared state across Route Handler invocations) and explicitly passes tokens through `client.request(refresh({ refresh_token }))` rather than relying on SDK-stored tokens.

This was a deliberate course-correction during the login feature's Step 3 — see [docs/features/login/step-3-origin-check-and-directus-auth.md](../features/login/step-3-origin-check-and-directus-auth.md) for the trade-off analysis.

---

## Deployment

Not yet deployed. The Fly slot `gevoelscore-frontend` exists; first deploy waits for the login feature to ship end-to-end (steps 5–7) so the live stack has something real to serve.

When ready: `fly deploy --app gevoelscore-frontend` from the repo root. The Dockerfile and fly.toml are already aligned with [ADR 0003](../decisions/0003-directus-fly-infra-setup.md):

- `NEXT_TELEMETRY_DISABLED=1` (no telemetry)
- `DIRECTUS_URL=https://gevoelscore-backend.fly.dev` (via the Fly proxy so a suspended backend wakes on request — [ADR 0007](../decisions/0007-self-hosted-postgres-on-fly.md); was `.internal` until 2026-07-14)
- Health check on `/api/health` every 30s
- Standalone Next build (~50MB runtime image)

---

## What this doc is NOT

- A tutorial — the setup is already done. This describes the result.
- An ADR — design decisions live in [`docs/decisions/`](../decisions/). This is the "what was wired up."
- A test-writing guide — see [`.claude/testing.md`](../../.claude/testing.md).

## References

- [ADR 0002](../decisions/0002-pwa-with-directus-backend.md) — stack
- [ADR 0003](../decisions/0003-directus-fly-infra-setup.md) — Fly deploy shape (Neon then; Fly Postgres since [ADR 0007](../decisions/0007-self-hosted-postgres-on-fly.md))
- [.claude/testing.md](../../.claude/testing.md) — testing doctrine
- [docs/features/login/](../features/login/) — first feature exercising every test layer
