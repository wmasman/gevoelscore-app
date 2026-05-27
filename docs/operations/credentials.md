# Credentials inventory

**This document holds LOCATIONS and ROTATION PROCEDURES — never values.** If you ever feel like pasting a real token or password here, stop. Pastebins, screenshots, AI chat transcripts, and PR diffs all leak.

The `.gitignore` at the repo root excludes `.env*` (with `.env.example` whitelisted) and `/private/` and `*.personal.*`. If you need a local file with real values, name it `.env.local` or put it under `/private/` — both are gitignored.

---

## Fly.io account

- **Login**: `fly auth login` (browser flow) → authenticated as `wmasman@gmail.com`
- **Token location**: stored by `flyctl` in `~/.fly/config.yml`. Never read or modify by hand.
- **Used for**: provisioning + deploying Fly apps; managing secrets; reading logs.
- **Rotation**: `fly auth logout` then `fly auth login`. Or revoke at https://fly.io/user/personal_access_tokens.

## Neon account

- **Login**: `neonctl me` (browser flow) → authenticated as `wmasman@gmail.com`
- **Token location**: stored by `neonctl` in `~/.config/neonctl/` (varies by platform). Never read or modify by hand.
- **Used for**: provisioning + managing Neon projects, branches, roles, passwords.
- **Rotation**: `neonctl auth logout` then `neonctl me` (login flow).

## Directus admin user (Fly secret + Directus DB)

| Item | Where it lives | Notes |
|------|---------------|-------|
| `ADMIN_EMAIL` | Fly secret on `gevoelscore-backend` | `wmasman@gmail.com`. Used by Directus only on bootstrap. |
| **Admin password** | Inside Directus (`directus_users.password`, bcrypt-hashed) | The bootstrap `ADMIN_PASSWORD` secret on Fly **should be unset** after first login. Verify with `fly secrets list --app gevoelscore-backend` — `ADMIN_PASSWORD` shouldn't appear. |
| **2FA TOTP secret** | Inside Directus (`directus_users.tfa_secret`, encrypted) | Tied to the admin user. To reset: log in via recovery, generate new QR in profile. |

**Rotating the admin password**: log into Directus admin UI → user profile → Password → change. No Fly secret update needed.

**Lost-2FA recovery**: if you lose your authenticator and don't have recovery codes saved, the only path back in is to clear `tfa_secret` directly in Postgres (via Neon SQL editor) — `UPDATE directus_users SET tfa_secret = NULL WHERE email = 'wmasman@gmail.com';` — then re-pair 2FA on next login.

## Directus static token (the one used by scripts)

| Item | Where |
|------|-------|
| Token value | Generated in Directus admin UI: User Profile → Token → Generate. Stored in your local shell as `$env:DIRECTUS_TOKEN` (PowerShell) or `export DIRECTUS_TOKEN=...` (bash), OR in `directus/.env.local` (gitignored). |
| Tied to | The admin user. Has full admin privileges. |
| Used for | Running `directus/scripts/*.mjs` against the live instance. |

**Rotation**: generate a new one in admin UI → the old one is revoked automatically. Update wherever you stored it. See [runbooks/rotate-credentials.md](runbooks/rotate-credentials.md).

**When to rotate**: any time it might have leaked (chat transcript, screenshot, copy-paste into a public channel, after sharing your machine).

## Directus internal secrets (Fly secrets on backend)

| Secret name | What it does | Rotation cadence |
|---|---|---|
| `KEY` | Directus encryption key — encrypts at-rest data Directus stores in Postgres (notes, content). Changing it breaks decryption of existing data. | Don't rotate unless compromise is suspected. If you must: export data → set new KEY → re-import. |
| `SECRET` | Signs Directus access/refresh JWTs. Changing it invalidates all active sessions (forces logout for everyone). | Same — only if compromise is suspected. |

These were generated as 32-byte hex strings at provisioning. Set via `fly secrets set --app gevoelscore-backend ...`. **Never stored anywhere locally.** If you lost them and need them back: `fly secrets list` shows the names but not the values; `fly machine ssh` into the running machine to read them from the process environment (last resort).

## Neon Postgres password

| Item | Where |
|------|-------|
| Role | `neondb_owner` |
| Password | Stored in Fly secret `DB_CONNECTION_STRING` on `gevoelscore-backend` (URL-embedded). The pooler endpoint variant is used. |
| Used by | Directus connecting to the database. |

**Rotation procedure** (full steps in [runbooks/rotate-credentials.md](runbooks/rotate-credentials.md)):

1. Generate new password in Neon console (Roles → `neondb_owner` → Reset password)
2. Build new connection string: `postgresql://neondb_owner:<NEW_PWD>@ep-flat-grass-alwa40oq-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require`
3. `fly secrets set DB_CONNECTION_STRING="<NEW_URI>" --app gevoelscore-backend` — Fly will redeploy machines automatically with the new value
4. Verify Directus comes back up: `curl https://gevoelscore-backend.fly.dev/server/info` → HTTP 200

## Frontend-app Directus user (does not exist yet)

Will be created manually via admin UI when wiring up the Next.js frontend. See [`../architecture/current-state.md`](../architecture/current-state.md) §"What's NOT yet done" step 1.

Credentials at that point:

- Email: separate from `wmasman@gmail.com` (e.g. `gevoelscore-frontend@yourdomain` or `wmasman+frontend@gmail.com` for Gmail aliasing)
- Password: random, store in password manager
- 2FA: enabled, store recovery codes in password manager
- Role: `gevoelscore-frontend-api` (already exists, see `current-state.md`)

The frontend logs in as THIS user, not the admin. Admin stays as recovery.

---

## What's in this transcript (2026-05-27 session)

For accountability, these three credentials were generated during the bootstrap session and are visible in the Claude Code chat transcript. **All should be rotated when convenient:**

1. Bootstrap admin password — already-or-soon-to-be replaced via Directus admin UI
2. Static Directus token (the one used by setup scripts) — rotate when you're done running schema scripts for a while
3. Neon DB password — rotate per the procedure above

The transcript itself is held in your Claude Code session history; you can clear it (`/clear`) when no longer needed.
