# Credentials inventory

**This document holds LOCATIONS and ROTATION PROCEDURES — never values.** If you ever feel like pasting a real token or password here, stop. Pastebins, screenshots, AI chat transcripts, and PR diffs all leak.

The `.gitignore` at the repo root excludes `.env*` (with `.env.example` whitelisted) and `/private/` and `*.personal.*`. If you need a local file with real values, name it `.env.local` or put it under `/private/` — both are gitignored.

---

## Fly.io account

- **Login**: `fly auth login` (browser flow) → authenticated as `user@example.com`
- **Token location**: stored by `flyctl` in `~/.fly/config.yml`. Never read or modify by hand.
- **Used for**: provisioning + deploying Fly apps; managing secrets; reading logs.
- **Rotation**: `fly auth logout` then `fly auth login`. Or revoke at https://fly.io/user/personal_access_tokens.

## Directus admin user (Fly secret + Directus DB)

| Item | Where it lives | Notes |
|------|---------------|-------|
| `ADMIN_EMAIL` | Fly secret on `gevoelscore-backend` | `user@example.com`. Used by Directus only on bootstrap. |
| **Admin password** | Inside Directus (`directus_users.password`, bcrypt-hashed) | The bootstrap `ADMIN_PASSWORD` secret on Fly **should be unset** after first login. Verify with `fly secrets list --app gevoelscore-backend` — `ADMIN_PASSWORD` shouldn't appear. |
| **2FA TOTP secret** | Inside Directus (`directus_users.tfa_secret`, encrypted) | Tied to the admin user. To reset: log in via recovery, generate new QR in profile. |

**Rotating the admin password**: log into Directus admin UI → user profile → Password → change. No Fly secret update needed.

**Lost-2FA recovery**: if you lose your authenticator and don't have recovery codes saved, the only path back in is to clear `tfa_secret` directly in Postgres (psql via `fly proxy 15432:5432 -a gevoelscore-pg`, or `fly machine exec` on the `gevoelscore-pg` machine — see [runbooks/rotate-credentials.md](runbooks/rotate-credentials.md) §Admin 2FA) — `UPDATE directus_users SET tfa_secret = NULL WHERE email = 'user@example.com';` — then re-pair 2FA on next login.

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

## Fly Postgres password

The database is the self-hosted Fly Postgres app `gevoelscore-pg` (since 2026-07-14, see [ADR 0007](../decisions/0007-self-hosted-postgres-on-fly.md)).

| Item | Where |
|------|-------|
| Role | `postgres` (superuser) |
| Password | Stored in Fly secret `DB_CONNECTION_STRING` on `gevoelscore-backend` (URL-embedded): `postgres://postgres:<password>@gevoelscore-pg.flycast:5432/gevoelscore`. The same password is embedded in `DATABASE_URL` in the gitignored `.env.local` (local proxy form). |
| Used by | Directus connecting to the database; local `pg`-based scripts via `fly proxy`. |

**Rotation procedure** (full steps in [runbooks/rotate-credentials.md](runbooks/rotate-credentials.md)):

1. Connect as `postgres` (via `fly proxy` or `fly machine exec`) and run `ALTER USER postgres WITH PASSWORD '<new>'`
2. `fly secrets set DB_CONNECTION_STRING="postgres://postgres:<new>@gevoelscore-pg.flycast:5432/gevoelscore" -a gevoelscore-backend` — Fly will redeploy machines automatically with the new value (~90 s)
3. Update `DATABASE_URL` in `.env.local`
4. Verify Directus comes back up: `curl https://gevoelscore-backend.fly.dev/server/info` → HTTP 200

## Frontend-app Directus user (does not exist yet)

Will be created manually via admin UI when wiring up the Next.js frontend. See [`../architecture/current-state.md`](../architecture/current-state.md) §"What's NOT yet done" step 1.

Credentials at that point:

- Email: separate from `user@example.com` (e.g. `gevoelscore-frontend@yourdomain` or `user+frontend@example.com` for Gmail aliasing)
- Password: random, store in password manager
- 2FA: enabled, store recovery codes in password manager
- Role: `gevoelscore-frontend-api` (already exists, see `current-state.md`)

The frontend logs in as THIS user, not the admin. Admin stays as recovery.

---

## What's in this transcript (2026-05-27 session)

For accountability, these three credentials were generated during the bootstrap session and are visible in the Claude Code chat transcript. **All should be rotated when convenient:**

1. Bootstrap admin password — already-or-soon-to-be replaced via Directus admin UI
2. Static Directus token (the one used by setup scripts) — rotate when you're done running schema scripts for a while
3. DB password — the Neon-era password died with Neon (decommissioned 2026-07-14); the Fly Postgres password rotates per the procedure above

The transcript itself is held in your Claude Code session history; you can clear it (`/clear`) when no longer needed.
