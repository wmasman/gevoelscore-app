# Security checklist — Next.js PWA + Directus

Loaded on demand by Claude when planning (`/plan-feature` Phase 5.3) or implementing (`/build-step` Phase 5.3). Linked from [CLAUDE.md](../CLAUDE.md).

Reference frames: **OWASP ASVS** (Application Security Verification Standard) for the web surface, plus the OWASP Top 10. Threat model: single-user app, self-hosted backend, personal health data — the threats are XSS / CSRF / secret-leak on the frontend, auth / CORS / injection on the backend, and supply-chain on both.

> **Curated, not exhaustive.** This list takes the parts of the TVO platform's security setup that apply to a single-user personal app, and drops the parts that don't (no public surface, no registration / forgot-password flow, no multi-role permissions). If a future feature changes that posture (e.g. opening the app to a second user), revisit this list before shipping.

---

## A01 — Broken Access Control

- [ ] Every Directus collection storing user data requires auth. No anonymous read of `day_entries`, `tags`, `projects`, `calendar_events`.
- [ ] The frontend uses a Directus role with **least privilege** — read/write only the collections it needs. Never the admin role.
- [ ] Static API tokens (if any) stored in Fly secrets, never committed, never in `NEXT_PUBLIC_*` env vars.
- [ ] Rotation: Directus admin password and any static tokens rotated when compromise is suspected. Document the rotation procedure once, not on a calendar cadence.

## A02 — Cryptographic Storage

- [ ] Session tokens in `httpOnly` + `Secure` + `SameSite=Strict` cookies. Never in `localStorage` / `sessionStorage` / JS-accessible cookies.
- [ ] OAuth refresh tokens (Google Calendar v1.5+) stored server-side in Directus, not exposed to the browser at all.
- [ ] Fly.io Postgres-at-rest encryption: Fly default. Confirmed enabled.

## A03 — Injection

- [ ] No `dangerouslySetInnerHTML` without a documented `@security` justification + DOMPurify sanitization.
- [ ] No user-controlled values in `href` / `src` / `style` attributes without validation.
- [ ] All Directus queries go through `src/lib/api/` using the `@directus/sdk` (parameterized). No string-concat SQL anywhere.
- [ ] **Boundary validation at every API surface** via domain validators in `src/lib/domain/*` returning the discriminated `Result<T, E>` shape. Strict-shape `REQUIRED_KEYS` checks reject missing or extra keys so a renamed Directus column surfaces immediately. Examples: `validateEpisode`, `validateTag`, `validateDayEntry`, `validateScore`. See [conventions.md §Code conventions](conventions.md#code-conventions) — "Boundary validation via domain validators" — for the full rule + when Zod scoped to a specific wide unstructured boundary (CSV import, LLM JSON, integration feeds) is acceptable.
- [ ] Token-format validation: any string treated as a token (Directus session, CSRF, OAuth code) is validated to the expected character set + length before use.

## A04 — Insecure Design

- [ ] Rate limiting on the login endpoint: **5 attempts per 5 minutes per IP**. Even single-user — bots probe every endpoint, and an obvious brute-force baseline costs almost nothing.
- [ ] No rate limit on read endpoints (single user, low volume) — Fly.io edge rate-limit catches anything pathological.
- [ ] Error responses are **generic**: "Invalid credentials" not "Password wrong" or "User not found". No stack traces, no internal paths.

## A05 — Security Misconfiguration

- [ ] **CORS on the Directus instance**: allow only the frontend's Fly.io origin. No wildcards. No localhost in production.
- [ ] **CSP headers** on the Next.js frontend: `default-src 'self'`, explicit allowlist for any third-party origin (none expected in v1).
- [ ] Security headers: `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` minimal.
- [ ] No source maps served in production.
- [ ] Debug / inspector routes gated by `process.env.NODE_ENV !== 'production'`. Return 404 in production builds.

## A07 — Authentication Failures

- [ ] Login uses Directus's password auth. No homegrown crypto.
- [ ] No "null" / "undefined" / "false" bypass vulnerabilities in auth checks (test these explicitly).
- [ ] Token expiry: Directus defaults are fine (15-min access, 7-day refresh). Document if changed.
- [ ] No forgot-password flow in v1 (single user, password set via Directus admin). If added later, re-enter this checklist.

## A08 — Data Integrity (CSRF)

- [ ] **CSRF approach**: `SameSite=Strict` cookies + server-side `Origin` / `Referer` validation on every state-changing request (POST / PUT / PATCH / DELETE). Reject if origin doesn't match the configured frontend origin.
- [ ] State-changing requests go through `src/lib/api/` so the origin-check pattern is enforced in one place.

## A09 — Logging & Monitoring

- [ ] No `console.log` of scores, notes, tags, or any user content in production. Dev-only logging gated by `process.env.NODE_ENV !== 'production'`.
- [ ] Error logs don't include the user's PII payload — log the error type and a stable ID, not the data that triggered it.

## Text-field handling (notes & tags)

The daily note is free-text Dutch from the user. Tags are short strings the user can edit. Both are stored verbatim in Postgres and rendered as plain text in the UI.

- [ ] Notes rendered as plain text only — React's default escaping is sufficient. **Do not** use `dangerouslySetInnerHTML` for notes in v1. If rich text is added in v2, route it through DOMPurify.
- [ ] Tags rendered as plain text in chip components. Same rule.
- [ ] **Soft client-side length cap** on notes: ~10,000 characters. Prevents accidental "paste-a-whole-document" UX failures. Show a clear counter when approaching the limit. The DB column is `text` (effectively unlimited), so this is purely a UX guard.
- [ ] **CSV export**: escape cells starting with `=`, `+`, `-`, `@`, or `\t` (prefix with `'`). Formula injection is the real risk when the user opens the export in Excel / Sheets. See ASVS 5.3.10.
- [ ] **CSV / XLSX import**: validate row by row before any write. Out-of-range scores, dates outside `[2022-09-03, today]`, wrong column count → reject the row with a clear error, never partial-write.

## PWA-specific

- [ ] Service worker cache strategy: sensitive responses (`/api/day-entries/*`, anything returning user data) use `network-first` or `network-only`. Never long-TTL cache.
- [ ] `manifest.webmanifest` carries no per-user state in `start_url` / `scope` / `name`.
- [ ] Install / "Add to Home Screen" prompt doesn't appear on screens that display personal notes.

## Supply chain

- [ ] `npm audit` shows zero high / critical before merging.
- [ ] Every new dep is checked: license (no GPL in MIT code), last-published date (no abandoned packages), maintainer reputation, transitive deps for telemetry.
- [ ] Lockfile committed. No floating versions.
- [ ] Architectural-tier deps (auth, storage, UI framework, test runner, anything crossing a layer) require an ADR. Utility libs get a one-line entry in `dependencies.md`.

---

## What this checklist deliberately drops vs. TVO's setup

- ❌ Per-route rate-limit presets (CONTENT 200/min, SEARCH 50/min, WRITE 20/min, SENSITIVE 5/5min) — single user, no traffic load. Login rate-limit only.
- ❌ Forgot-password / reset-password flow rate limits — there is no forgot-password flow in v1.
- ❌ `knownRoutes` / `publicRoutes` / `adminOnlyRoutes` split — there are no public routes; everything requires auth.
- ❌ Field-level Directus permissions for hiding admin fields from public — no public access at all.
- ❌ 90-day calendar-driven token rotation — single admin, rotate on suspicion, document the procedure.
- ❌ Double-submit-cookie CSRF token (chosen `SameSite=Strict` + Origin check instead — simpler, fits the threat model).

If a future feature opens the app to a second user, public read access, or an unattended OAuth callback, revisit this list — the dropped items become relevant again.
