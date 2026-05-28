# ADR 0005: Frontend session persistence via Directus collection

- **Status**: Accepted
- **Date**: 2026-05-28
- **Builds on**: [ADR 0002](0002-pwa-with-directus-backend.md) (Directus-backed stack), [ADR 0003](0003-directus-fly-infra-setup.md) (single Fly machine, in-memory module singletons)
- **Deciders**: Willem Masman (author), Claude (AI collaborator)

## Context

The login feature shipped in 2026-05-27 with a module-singleton in-memory `SessionStore` — a plain `Map<sessionId, { accessToken, refreshToken, expiresAt }>` living in `src/lib/auth/stores.ts`. The decision was deliberate (ADR 0003 §"Single-process Fly machine"): one app process, no horizontal scaling planned in v1, and the cookie carried only an opaque id so the actual tokens never reached the browser.

Three months of dogfooding later, on **2026-05-28**, the user reported the timeline tab on their phone showed an empty calendar despite Directus containing 1,364 day-entries. Investigation revealed two layered bugs:

1. **`page.tsx` had only one redirect guard.** It checked `sessionId === null` (cookie missing) and redirected. It did *not* redirect when `sessionId` was present but `getValidatedSession(sessionId)` returned `null` (cookie there, store empty). Instead, it rendered the shell with `entry = null`, `allTags = []`, `timelineEntries = []` — visually indistinguishable from a fresh-install screen, and with no signal to the user.

2. **The in-memory store loses every session on every restart.** Fly machine restarts (three in one day on the 28th: deploy, manual restart, deploy) wipe the `Map`. Cookies the browser still holds resolve to nothing. The first bug then ensured the user saw a calendar shaped like there was no data, when in fact there was no *session*.

Independent of the timeline UX, the same pattern is at work in every deploy: every push logs the user out. Acceptable when the user is also the developer and deploys are rare; not acceptable as the app stabilises and deploys become operations, not features.

The user picked the **Directus collection** option (see [investigation thread 2026-05-28](../audits/2026-05-28-daily-entry-audit.md#l25-session-persistence-across-fly-restarts)) over a stateless signed-cookie design and over a Fly-volume file store.

## Options considered

### Option A — Directus collection (chosen)

Add a `frontend_sessions` table to the existing Directus instance. Sessions persist across Fly restarts because Directus + Neon do. The `SessionStore` interface stays the same; only the implementation behind it changes (and becomes async — see "Consequences" below).

**Pros**
- Reuses the existing data plane. No new infrastructure (no Redis, no Fly volume, no new SaaS).
- Survives every Fly restart, including the ones the developer doesn't initiate (host maintenance, OOM kills).
- Inspectable and revocable through the Directus admin UI — single-place to "log everyone out" if a token leaks.
- Operates within the GDPR Article 9 envelope the user has already declared for `day_entries`. Tokens sit in the same database under the same encryption-at-rest posture (Neon).

**Cons**
- Every API request that touches the session does a Directus round trip (~10–20 ms on the internal Fly Wireguard network). Acceptable for a single-user app; revisit if multi-user-with-load lands.
- Requires a service token on the Fly frontend machine to talk to Directus *before* the user has authenticated. For v1 this is the existing admin static token, which is over-privileged — flagged as a follow-up (see "Open follow-ups").
- The `SessionStore` interface had to migrate from sync to async, touching every call site.

### Option B — Stateless signed cookies (NextAuth pattern)

Encrypt the access + refresh tokens into the cookie itself, signed with a server-held secret. No server-side store at all.

**Pros**
- Survives every restart trivially — there is no server state to lose.
- Zero per-request latency overhead.
- Conceptually clean: the cookie is the session.

**Cons**
- Browser sees a substantial encrypted blob (~400–500 bytes) instead of an opaque 36-char uuid. Still well under the 4 KB cookie cap, but cookie size is sent on every request.
- Hard to revoke a single session out-of-band — the only way to invalidate a stateless token is to rotate the signing key, which invalidates *every* session.
- Net architectural change is bigger: the existing `SessionStore` abstraction goes away entirely instead of getting a new backing implementation. More churn in the codebase, more places to slip up.
- Loses the inspectability + revocation affordance of having sessions visible in Directus admin.

### Option C — Fly volume + JSON-file store

Mount a Fly volume on the frontend machine, write the session `Map` to a JSON file on every mutation, read it on boot.

**Pros**
- No network. Lowest per-request latency.
- No service token needed.

**Cons**
- ADR 0002 deliberately avoided introducing new persistence layers beyond Directus. This would re-introduce one.
- Fly volumes pin a machine to a region and complicate horizontal scaling later.
- File-locking semantics during concurrent writes need handling. Single-process safe today but a footgun later.
- Backup story is separate from Directus backups, which already cover the user's data.

## Decision

**Option A — Directus collection.** Specifically:

- A new `frontend_sessions` collection with fields `{ id (uuid PK, app-generated), access_token (text), refresh_token (text), expires_at (timestamp), created_at (date-created) }`. Created idempotently by `directus/scripts/setup-frontend-sessions.mjs`.
- Permissions granted on the existing `gevoelscore-frontend-policy` (CRUD on `frontend_sessions` only).
- A new `createDirectusSessionStore` in `src/lib/auth/directus-session-store.ts` implementing the same `SessionStore` interface as the in-memory store, but every method `async`.
- `src/lib/auth/stores.ts` selects the implementation at module-init time: Directus-backed when both `DIRECTUS_URL` and `DIRECTUS_TOKEN` are set, in-memory otherwise. Tests and minimal local setups continue to use the in-memory implementation transparently.
- `src/app/page.tsx` now redirects to `/login` on *both* missing-cookie and missing-session-in-store. The "render empty shell" branch is gone.
- The `DIRECTUS_TOKEN` service token is provisioned on `gevoelscore-frontend` as a Fly secret.

Tokens are stored in plaintext for v1. The threat model: the database is the user's own self-hosted Directus, and a breach there already exposes the source data. Field-level encryption with a key held outside Directus would protect against an attacker who reads the DB but not the frontend machine, which is a narrow attack class for a single-user PWA. Revisit if multi-user lands.

## Consequences

### Interface change: `SessionStore` is now async

Every method on `SessionStore` returns a `Promise`. Call sites — `get-validated-session.ts`, `/api/auth/login/route.ts`, `/api/auth/login/verify/route.ts`, `/api/auth/logout/route.ts` — all now `await` store operations. The in-memory `createSessionStore` was updated to match (its methods just return resolved Promises). This was a one-time migration; the interface is now stable.

### Per-request latency: +10–20 ms

Every `getValidatedSession()` call hits Directus over the internal Fly Wireguard. Measured at ~15 ms median against `gevoelscore-backend.fly.dev` from `gevoelscore-frontend` (Amsterdam ↔ Amsterdam). Well inside the cardinal sub-10s budget; not noticeable in the daily-entry save loop (the score wheel's 500 ms debounce dominates).

### Testing surface

A new test class — *process-state tests* — was added to [.claude/testing.md](../../.claude/testing.md). The recipe pins down two scenarios that every persistence layer must satisfy:

1. **Page-level redirect coverage** ([src/app/__tests__/page.test.ts](../../src/app/__tests__/page.test.ts)): a server-component test asserts all three branches (no cookie / cookie + null session / cookie + valid session) take the right path. This is the test that, had it existed, would have caught the original bug.
2. **Cross-instance store contract** ([src/lib/auth/__tests__/directus-session-store.test.ts](../../src/lib/auth/__tests__/directus-session-store.test.ts)): a test asserts that a brand-new store instance reads sessions written by an earlier instance. This is the Fly-restart invariant in unit-test form.

The lesson generalises: any module-singleton that a client identifier points into needs both a "what happens if the process restarted" test and a "where does the empty case route" test.

### Deployment cost

One new Fly secret on `gevoelscore-frontend` (`DIRECTUS_TOKEN`). One Directus migration (the `setup-frontend-sessions.mjs` script). Both are idempotent and reversible — dropping back to in-memory is one env-var unset + one process restart away.

### What this ADR does NOT decide

- It does not introduce session revocation UX. The admin-UI revoke affordance is implicit (delete the row), but no in-app "log out all devices" feature is added.
- It does not change the cookie surface (`gs_session` cookie shape, `HttpOnly`, `Secure`, `SameSite=Strict`, `Max-Age` 30 days are all unchanged).
- It does not address the in-memory `pendingOtpStore` / `pendingTfaStore` / rate limiters. Pending stores are 5-minute TTL — a restart-induced wipe is at worst a re-login for an in-flight 2FA flow. Rate-limit wipes give a single attacker a fresh window per restart, which is bounded by deploy frequency, not a meaningful attack amplification.

## Open follow-ups

1. **Scope the runtime Directus token.** The token currently on `gevoelscore-frontend` is the full admin static token. Acceptable for v1 ship-soak; not acceptable as a long-term posture. Create a dedicated Directus user with a role whose policy is restricted to `frontend_sessions` CRUD only. Tracked in [docs/plans/2026-05-27-audit-remediation-and-standards-enforcement.md A3](../plans/2026-05-27-audit-remediation-and-standards-enforcement.md#a3--priority-3-compliance--observability-this-quarter).

2. **Field-level encryption of tokens.** Once a second user enters the picture (v1.5+), encrypt `access_token` and `refresh_token` with a KMS-held key. Cheap to add later because the only consumer is the store wrapper.

3. **Playwright "two browsers + restart" spec.** The Vitest recipes pin the contract; a real end-to-end "log in, kill server, restart, reload, still works" test would close the loop. Deferred until Playwright fixtures for restart-during-spec land — currently the cost exceeds the marginal value.

## Status of the originating bug

- **Surface bug** (silent empty shell): closed by the `page.tsx` second redirect. Test in [page.test.ts](../../src/app/__tests__/page.test.ts).
- **Root cause** (in-memory store wiped on restart): closed by this ADR's chosen option. Test in [directus-session-store.test.ts](../../src/lib/auth/__tests__/directus-session-store.test.ts).
- **Class of bug** (silent-empty-default-on-server-state-loss): covered by the new "Process-state tests" section in [.claude/testing.md](../../.claude/testing.md).
