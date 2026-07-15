# Runbook: rotate credentials

Procedures for rotating every credential listed in [`../credentials.md`](../credentials.md).

**General rule**: rotate any credential that has been exposed (chat transcript, screenshot, copy-paste into a public channel, shared machine). Rotation is cheap; suspicious credentials are not.

---

## Static Directus admin token

The token used by `directus/scripts/*.mjs` to provision schema, seed tags, run migrations.

**Important:** since 2026-05-30 the frontend Fly app uses a **scoped** Directus token, NOT the admin token (see "Scoped frontend-sessions token" below). Rotating the admin token does NOT log users out and does NOT require touching `gevoelscore-frontend` Fly secrets. Only your local scripts and `directus/.env.local` care.

1. Open https://gevoelscore-backend.fly.dev/admin
2. User Profile → **Token** → Generate (this revokes the previous token)
3. Copy the new value
4. Wherever you stored the old one, replace it:
   - `$env:DIRECTUS_TOKEN` in your active shell
   - `directus/.env.local` if you use one (gitignored)
   - `.env.local` at the project root if your local scripts use it
   - Any active terminal/process that read the old one — they're now using a dead token, restart them
5. Verify with: `curl -H "Authorization: Bearer <new>" https://gevoelscore-backend.fly.dev/users/me` → HTTP 200

**Time**: ~2 minutes.

---

## Auth smoke — the integration check that unit tests can't

Run this before pushing any auth-touching change, and after any Fly secret swap involving `DIRECTUS_TOKEN`, `SESSION_TOKEN_KEY`, or `WILLEM_USER_ID`. ~3 s. Catches the integration regressions unit tests can't see (e.g. on 2026-05-31 a wrong `WILLEM_USER_ID` value silently rejected every legit login — would have been caught here immediately).

### Setup (once)

Add to `.env.local` (gitignored):

```
WILLEM_EMAIL=user@example.com
WILLEM_PASSWORD=<your password>
```

### Run

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-auth-smoke.ps1
```

Exits 0 on PASS, 1 on FAIL. Output lists each check with ✓/✗.

The script exercises: login → cookie set → authenticated read of `/api/day-entries/today` → logout → 401-after-logout. If 2FA is on for the smoke user the script exits with code 3 and a note (extend the script with OTP, or temporarily disable 2FA for the smoke target).

---

## Scoped frontend-sessions token

The token used by the Next.js frontend Fly app to read/write the `frontend_sessions` collection (audit S-H1, 2026-05-30). Lives in Fly secret `DIRECTUS_TOKEN` on app `gevoelscore-frontend`. Anchored to the service user `frontend-sessions-service@gevoelscore.internal` whose role (`gevoelscore-frontend-sessions-service-role`) has CRUD on `frontend_sessions` only — nothing else.

### When to rotate

- Audit, periodically (every 90 days is sensible).
- After any exposure: copy-paste into a public channel, screenshot, shared machine.
- Immediately after the very first provisioning (script's initial run mints one token; the rotation script overwrites it on every run).

### Procedure

The script is **idempotent** — running it again rotates the token. It does NOT touch the policy, role, user, or permissions if they're already correct.

```powershell
# 1. Set the admin token (NOT the scoped token) — this script needs admin to mutate /policies, /roles, /users, /access.
$env:DIRECTUS_TOKEN = "<admin static token>"

# 2. Run the rotation script.
node directus/scripts/setup-frontend-sessions-service-token.mjs
# Prints the new token at the bottom. Capture it.

# 3. Set it on Fly. Triggers a rolling redeploy (~90 s).
fly secrets set DIRECTUS_TOKEN="<new token>" -a gevoelscore-frontend

# 4. Verify the session store still works:
#    - Open https://gevoelscore-frontend.fly.dev/ in a private window.
#    - Log in.
#    - Reload the page. If you stay logged in, the new scoped token is live.

# 5. (Optional) If you rotated because of exposure, also clear any
#    sessions that were issued under the compromised token:
#    Open Directus admin UI → frontend_sessions → select all → Delete.
#    The user re-logs in on next request.
```

**Time**: ~5 minutes including the Fly redeploy and verification.

### Recovery: scoped token lost / wrong

If `DIRECTUS_TOKEN` on Fly is missing or wrong, the frontend can't read `frontend_sessions` and every authenticated request returns 401 (the user gets redirected to `/login`). To recover: just re-run step 2-3 above. The script is non-destructive — re-running mints a fresh token that overwrites the broken one.

---

## Admin user password

The password for logging into the Directus admin UI as the bootstrap admin user (email stored in 1Password under "gevoelscore — Directus admin").

1. Log into Directus admin UI
2. User Profile → **Password** → set new password
3. Save in your password manager
4. If `ADMIN_PASSWORD` is still set as a Fly secret on the backend (it shouldn't be after bootstrap, but check): `fly secrets unset ADMIN_PASSWORD --app gevoelscore-backend`

The Fly secret is only consulted on Directus startup for bootstrap; the live password is stored hashed inside Directus's own DB.

**Time**: ~1 minute.

---

## Admin 2FA (TOTP)

If you lost your authenticator app:

**Option A: you still have a working static token.** Use the API to clear `tfa_secret`:

```powershell
# Replace <admin-user-uuid> with the bootstrap admin's UUID (look up via
# Directus admin UI → Settings → Access Control → Users, or via the
# directus_users table).
curl -X PATCH -H "Authorization: Bearer <static token>" `
  -H "Content-Type: application/json" `
  -d '{"tfa_secret":null}' `
  https://gevoelscore-backend.fly.dev/users/<admin-user-uuid>
```

Then log into admin UI, re-pair 2FA in your profile.

**Option B: no static token either.** Run the SQL directly against Postgres. psql lives on the `gevoelscore-pg` machine (note: Postgres listens on 5433 there — 5432 is haproxy):

```powershell
# Replace <admin-email> with the bootstrap admin's email (from 1Password).
# <password> is the postgres password embedded in the DB_CONNECTION_STRING secret / .env.local.
fly machine exec 830999a71e2ee8 "psql postgres://postgres:<password>@localhost:5433/gevoelscore -c \"UPDATE directus_users SET tfa_secret = NULL WHERE email = '<admin-email>';\"" -a gevoelscore-pg
```

Alternatively, run `fly proxy 15432:5432 -a gevoelscore-pg` in one terminal and issue the same `UPDATE` through a `pg`-based script using the `DATABASE_URL` from `.env.local` (local Windows has no psql).

Then log in with password, re-pair 2FA.

**Prevention**: save the recovery codes Directus shows during the initial 2FA setup. Store them in your password manager.

---

## Fly Postgres database password

Used by Directus to connect to Postgres (self-hosted `gevoelscore-pg` since 2026-07-14, see [ADR 0007](../../decisions/0007-self-hosted-postgres-on-fly.md)). Lives in Fly secret `DB_CONNECTION_STRING` on `gevoelscore-backend` (URL-embedded); the same password is embedded in `DATABASE_URL` in the gitignored `.env.local` (proxy form).

### Procedure

1. **Set a new password** — connect as `postgres` and run `ALTER USER`. Via the machine (psql lives there; Postgres listens on 5433 — 5432 is haproxy):
   ```powershell
   fly machine exec 830999a71e2ee8 "psql postgres://postgres:<old-password>@localhost:5433/gevoelscore -c \"ALTER USER postgres WITH PASSWORD '<new>'\"" -a gevoelscore-pg
   ```
   Or via the local proxy (`fly proxy 15432:5432 -a gevoelscore-pg` in one terminal) with a `pg`-based script.

2. **Update the Fly secret** (this triggers a rolling redeploy, ~90 s):
   ```powershell
   fly secrets set DB_CONNECTION_STRING="postgres://postgres:<new>@gevoelscore-pg.flycast:5432/gevoelscore" -a gevoelscore-backend
   ```

3. **Update `DATABASE_URL` in `.env.local`** (proxy form):
   ```
   DATABASE_URL=postgres://postgres:<new>@127.0.0.1:15432/gevoelscore
   ```

4. **Verify Directus comes back up**:
   ```powershell
   curl https://gevoelscore-backend.fly.dev/server/info
   # Expected: HTTP 200, shortly after the redeploy completes
   ```

5. If the deploy fails (Directus can't connect with the new password): you've likely fat-fingered the connection string. Re-check the URL-encoding (passwords with `@`, `:`, `/`, `?` need URL-encoding).

**Time**: ~5 minutes including the redeploy.

---

## Directus `KEY` and `SECRET` (rare)

Don't rotate these unless you've concluded they leaked.

- `KEY` is the at-rest encryption key. Rotating it breaks decryption of any data Directus encrypted at rest (some special fields, secrets stored via the Directus secrets API).
- `SECRET` signs JWTs. Rotating it invalidates all active sessions.

If you must rotate `SECRET` (compromise of session tokens):

```powershell
$new = -join ((48..57) + (97..102) | Get-Random -Count 64 | ForEach-Object { [char]$_ })
fly secrets set SECRET=$new --app gevoelscore-backend
```

Everyone logged in (you, the future frontend user) will be forced to log in again. No data loss.

If you must rotate `KEY` (compromise of at-rest encryption):

1. Export all data: `npx directus schema snapshot` + dump Postgres
2. Set new `KEY`
3. Re-import data
4. This is invasive — talk it through with someone (or your future self in a calm moment) before doing it.

---

## Fly access token

If your `fly auth` token leaks (e.g. you logged in on someone else's machine and forgot to log out):

```powershell
fly auth logout
fly auth login
```

Or, more aggressively, revoke all tokens via the web UI (https://fly.io/user/personal_access_tokens).
