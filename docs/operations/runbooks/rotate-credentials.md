# Runbook: rotate credentials

Procedures for rotating every credential listed in [`../credentials.md`](../credentials.md).

**General rule**: rotate any credential that has been exposed (chat transcript, screenshot, copy-paste into a public channel, shared machine). Rotation is cheap; suspicious credentials are not.

---

## Static Directus admin token

The token used by `directus/scripts/*.mjs`.

1. Open https://gevoelscore-backend.fly.dev/admin
2. User Profile → **Token** → Generate (this revokes the previous token)
3. Copy the new value
4. Wherever you stored the old one, replace it:
   - `$env:DIRECTUS_TOKEN` in your active shell
   - `directus/.env.local` if you use one (gitignored)
   - Any active terminal/process that read the old one — they're now using a dead token, restart them
5. Verify with: `curl -H "Authorization: Bearer <new>" https://gevoelscore-backend.fly.dev/users/me` → HTTP 200

**Time**: ~2 minutes.

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

**Option B: no static token either.** Open the Neon SQL editor (console.neon.tech → gevoelscore-db → SQL Editor) and run:

```sql
-- Replace <admin-email> with the bootstrap admin's email (from 1Password).
UPDATE directus_users SET tfa_secret = NULL WHERE email = '<admin-email>';
```

Then log in with password, re-pair 2FA.

**Prevention**: save the recovery codes Directus shows during the initial 2FA setup. Store them in your password manager.

---

## Neon database password

Used by Directus to connect to Postgres. Lives in Fly secret `DB_CONNECTION_STRING` (URL-embedded).

### Procedure

1. **Reset the password in Neon**:
   ```powershell
   neonctl roles reset-password neondb_owner --project-id <project-id>
   # OR: console.neon.tech → gevoelscore-db → Roles → neondb_owner → Reset password
   ```
   Copy the new password. **Now's your only chance — Neon won't show it again.**

2. **Build the new connection string** using the pooler endpoint:
   ```
   postgresql://neondb_owner:<NEW_PWD>@ep-flat-grass-alwa40oq-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require
   ```

3. **Update the Fly secret** (this triggers a rolling redeploy):
   ```powershell
   fly secrets set DB_CONNECTION_STRING="<new URI>" --app gevoelscore-backend
   ```

4. **Verify Directus comes back up**:
   ```powershell
   curl https://gevoelscore-backend.fly.dev/server/info
   # Expected: HTTP 200, ~30s after the deploy completes
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

## Fly access token / Neon access token

If your `fly auth` or `neonctl me` token leaks (e.g. you logged in on someone else's machine and forgot to log out):

```powershell
fly auth logout
fly auth login

neonctl auth logout
neonctl me   # triggers re-login
```

Or, more aggressively, revoke all tokens via the web UIs (https://fly.io/user/personal_access_tokens, https://console.neon.tech → Settings → API keys).
