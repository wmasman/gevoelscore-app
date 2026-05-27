# Step 8: Live-stack Playwright (production build + real Directus)

**Estimated time:** 1.5–2 hours
**Test layer:** Playwright integration against `next start` + real `gevoelscore-backend.fly.dev`.
**Risk:** Medium — depends on a real Directus user account and credentials in `.env.local`. The frontend itself is NOT deployed; only the Next.js build runs locally.
**Prerequisite:** Steps 1–7 done.

> Closes the login feature. Two coverage gaps the earlier steps couldn't fill:
> 1. `next dev` re-evaluates server modules between requests — module-singleton state (rate limiter, session map) doesn't persist. `next start` doesn't have this problem. Two specs from Step 4 were skipped waiting for this.
> 2. Mocked SDK responses approximate Directus's real error shapes. Real-Directus runs validate the actual `INVALID_CREDENTIALS` / `INVALID_OTP` envelopes, the cookie attributes the server emits, and the refresh-token invalidation flow.

---

## Acceptance criteria

- [ ] AC5 (full): 6th `/api/auth/login` POST from the same IP within 5 minutes returns 429 — verified against `next start`, not `next dev`.
- [ ] AC8 (full): Same for `/api/auth/login/verify`.
- [ ] AC1/AC3 (real-Directus): `/api/auth/login` with bad credentials returns 401 `{ error: 'invalid_credentials' }`. The Directus error envelope is correctly decoded by `directus-auth.ts` against the actual response.
- [ ] AC2 (real-Directus): `/api/auth/login` with valid credentials against a 2FA-enabled account returns `{ requires_otp: true }` + sets `gs_pending_otp` cookie. (Full OTP completion in automation requires a TOTP library; out of scope. Manually verified once.)
- [ ] AC11 (real cookies): The session cookie emitted by `/api/auth/login` happy-path has all the correct attrs against a real session (HttpOnly + Secure-where-applicable + SameSite=Strict + Path=/).

## Out of scope

- **Automating the full 2FA OTP submit** — would need a TOTP-from-secret helper as a test dep. Manually verified on first run.
- **Deploying the frontend to Fly** — that's a separate concern; see `fly.toml` + ADR 0003 when ready.
- **Cleanup of test sessions in Directus** — tests POST logout after any successful login to invalidate the refresh token; orphaned tokens would be a problem only at scale.

## Prerequisites — manual setup before this step runs

### 1. Create the frontend-app Directus user (one-time, ~10 min)

Visit `https://gevoelscore-backend.fly.dev/admin` and log in with the admin account, then:

- Settings → Access Control → Users → **+ Create User**
- First name: e.g. `Gevoelscore Frontend` (anything)
- Email: pick an inbox you control (e.g. `wmasman+gevoelscore@gmail.com` if your provider supports plus-addressing)
- Password: strong random; **store in your password manager**
- Role: `gevoelscore-frontend-api`
- Status: Active
- Save. **Do NOT enable 2FA yet** — you'll do that via `/login/2fa-setup` after first login.

### 2. Create `.env.local` at the repo root (gitignored)

```
PLAYWRIGHT_TEST_EMAIL=<the email above>
PLAYWRIGHT_TEST_PASSWORD=<the password above>
```

(The repo's `.gitignore` already excludes `.env*` except `.env.example`.)

### 3. Run the step

```powershell
npm run test:live
```

This runs `next build && next start` then executes the specs in `tests/live-stack/`. Slower than `test:e2e` (real production build, ~30s startup) but accurate.

---

## Plan

### 8.1 `playwright.live-stack.config.ts`

A second Playwright config (parallel to `playwright.config.ts`):

- Different `testDir` → `./tests/live-stack`
- `webServer.command: 'npm run build && npm run start'`
- `webServer.env` overrides:
  - `DIRECTUS_URL=https://gevoelscore-backend.fly.dev`
  - `NODE_ENV=production`
- `webServer.timeout: 180_000` (the build takes a while)
- No `webServer.env` for the unreachable Directus — we WANT the real one here.

### 8.2 Specs

- `tests/live-stack/rate-limit.spec.ts` — unskips the two specs from Steps 4: 6 attempts from one IP → 429; separate buckets for login vs verify.
- `tests/live-stack/auth.spec.ts` — uses the credentials from `.env.local`:
  - Bad password against real account → 401 `{ error: 'invalid_credentials' }`.
  - Right password against (eventually) 2FA-enabled account → `{ requires_otp: true }` + cookie set.
  - Cookie attrs verified.

### 8.3 npm script

Add `"test:live": "playwright test --config=playwright.live-stack.config.ts"` to `package.json`. Doesn't run as part of `test:all` — it's intentional, manual.

---

## Done criteria

- [x] All live-stack specs pass against `gevoelscore-backend.fly.dev` (4/4)
- [x] Existing Vitest + dev-mode Playwright still green (Vitest 342/342, Playwright dev 45 + 2 skipped — the 2 were the ones we just *un*skipped here, so they remain skipped in dev mode where they belong)
- [x] Typecheck + lint clean
- [ ] Optional — once verified working in practice, enable 2FA on the test account via `/login/2fa-setup` for full security parity with prod usage

### Captured evidence

- **First green run**: 4/4 in 30 seconds (~28s for the production build, ~2s for the actual tests).
  - `AC3: invalid credentials return 401 invalid_credentials (real Directus envelope)` ✓
  - `AC1 or AC2: valid credentials yield either {ok:true} + session cookie OR {requires_otp:true} + pending cookie` ✓
  - `AC5: 6th attempt within 5 minutes from same IP returns 429` ✓
  - `AC8: separate rate-limit buckets for /login vs /login/verify` ✓
- **Real Directus error envelopes decoded correctly** — confirms our `errorCode()` helper in [directus-auth.ts](../../../src/lib/auth/directus-auth.ts) matches the actual `{ errors: [{ extensions: { code: 'INVALID_CREDENTIALS' } }] }` shape.

### Side-quest: `next start` vs `output: 'standalone'` warning

The webServer runs `npm run build && npm run start`. Next emits a warning during start:

```
⚠ "next start" does not work with "output: standalone" configuration.
   Use "node .next/standalone/server.js" instead.
```

The tests pass anyway — `next start` falls back to serving from `.next/` even though the standalone bundle was produced. Decision: **keep `next start`** for the test runner because:

1. The standalone server requires copying `.next/static` and `public/` into `.next/standalone/` — easy in the Dockerfile (multi-stage `COPY`), awkward in a cross-platform npm script.
2. The auth flow behaviour we're testing is identical between the two server modes.
3. The production deploy on Fly uses the standalone bundle correctly (see [Dockerfile](../../../Dockerfile)) — that path is exercised on deploy, not in tests.

If we ever need exact-Docker parity in tests (e.g., a future bundling regression we want to catch), revisit then.
