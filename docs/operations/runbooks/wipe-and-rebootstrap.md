# Runbook: wipe Neon DB and re-bootstrap

The nuclear option. Used when the schema is in a state that's too tangled to fix surgically.

**Before you do this**: try the surgical fix first.

- "Wrong PostgreSQL type on field X" → delete that field in Directus admin UI, re-run `setup-schema.mjs` (the script re-creates the field correctly).
- "Permissions weird" → delete the policy in admin UI, re-run `setup-permissions.mjs`.
- "Stuck Directus migration" → check `fly logs --app gevoelscore-backend`, often a Postgres connection blip; restart the machine.

If those don't fix it, proceed.

---

## ⚠ This destroys all user data

The wipe drops the Neon database. Any `day_entries`, `tags`, `projects`, etc. that you've added are gone. **Export anything you want to keep first**:

```powershell
neonctl connection-string gevoelscore-db --psql
# Use the printed psql command to dump:
pg_dump --no-owner --no-acl --clean --if-exists --schema=public > backup-$(date +%Y-%m-%d).sql
```

Or create a Neon branch — instant snapshot you can restore from:

```powershell
neonctl branches create --project-id <id> --name pre-wipe-$(date +%Y-%m-%d)
```

---

## Procedure

### 1. Stop the backend (optional but cleaner)

```powershell
fly scale count 0 --app gevoelscore-backend --yes
```

Prevents Directus from trying to reconnect during the wipe.

### 2. Wipe the Neon database

**Option A: drop and re-create the database** (preserves the Neon project, role, password):

```powershell
neonctl databases delete neondb --project-id <project-id>
neonctl databases create --name neondb --project-id <project-id> --owner-name neondb_owner
```

**Option B: nuke and re-create the entire Neon project** (gives you a fresh password, requires updating Fly secrets):

```powershell
neonctl projects delete <project-id> --confirm
neonctl projects create --name gevoelscore-db --region-id aws-eu-central-1 --org-id <org-id>
# Take the new connection string → fly secrets set DB_CONNECTION_STRING=... --app gevoelscore-backend
```

Option A is usually enough. Option B is for "I think my Neon project metadata is corrupted" scenarios.

### 3. Start the backend again

```powershell
fly scale count 1 --app gevoelscore-backend --yes
fly logs --app gevoelscore-backend --no-tail | Select-Object -Last 30
```

Directus will detect the empty DB and **auto-run all its internal migrations on startup** (~10–20 seconds). You should see logs like `INFO: Applying Add Focalpoints…` through `INFO: Adding first admin user…`.

If `ADMIN_EMAIL` and `ADMIN_PASSWORD` are set in Fly secrets, Directus creates the admin user automatically. If not (you `fly secrets unset ADMIN_PASSWORD` after the original bootstrap), you'll need to re-set them before this step.

### 4. Log back in + re-enable 2FA

The new admin user has the password from the Fly `ADMIN_PASSWORD` secret. Log in, change it, re-enable 2FA, generate a new static token. See [rotate-credentials.md](rotate-credentials.md).

### 5. Re-run schema + permissions

```powershell
$env:DIRECTUS_TOKEN = "<new static token>"

node directus/scripts/setup-schema.mjs       # creates the 9 collections + 2 M2M junctions (with provenance + tag hierarchy)
node directus/scripts/verify-schema.mjs      # confirms 29/29 PG types
node directus/scripts/setup-permissions.mjs  # creates role + policy + 24 permissions
```

The one-time historical migrations (`upgrade-m2m-tags.mjs`, `add-tag-provenance.mjs`, `flatten-day-entry-json-arrays.mjs`, `add-tag-hierarchy.mjs`) are **NOT** re-run on a fresh wipe — their end state is baked into `setup-schema.mjs`.

If everything passes, you're back to a clean v1 schema state.

### 6. Re-apply the Postgres views

Paste each file from [`directus/scripts/views/`](../../../directus/scripts/views/) into the Neon Console SQL editor, or `psql -f` if available. All three views use `CREATE OR REPLACE` — re-applying is safe.

### 7. Re-seed reference data

```powershell
node directus/scripts/seed-tags.mjs           # 83 tags from lib/tag-patterns.mjs
node directus/scripts/seed-projects.mjs       # the 5 v1 projects
```

### 8. Re-import historical data

```powershell
# Requires private/real-history.csv (gitignored — restore from your local copy)
node directus/scripts/import-real-history.mjs --commit
node directus/scripts/recompute-tag-usage.mjs
```

### 9. Verify backend health

```powershell
curl https://gevoelscore-backend.fly.dev/server/info
# Expected: HTTP 200
```

---

## How long this takes

- Backup snapshot: 30 seconds (Neon branching is fast)
- Wipe + recreate DB: 30 seconds
- Backend restart + Directus migrations: ~30 seconds
- Re-running schema/permissions scripts: ~30 seconds
- Admin login + 2FA setup: ~5 minutes

Total: ~10 minutes if everything goes smoothly. Plan for 30 minutes if you're stressed.

---

## Things that go wrong

| Symptom | Cause | Fix |
|---|---|---|
| `setup-schema.mjs` says "FORBIDDEN" | Static token tied to old user (deleted) | Generate a new token in admin UI |
| Backend won't start after wipe | `ADMIN_PASSWORD` was unset; Directus has no admin to create | `fly secrets set ADMIN_PASSWORD=<temporary>`, restart, log in, change password, unset secret again |
| `verify-schema.mjs` fails on some field | The schema script was modified between wipes, drift between expected and actual | Update either the script or `verify-schema.mjs`'s expectations table |
| The Neon DB doesn't actually empty | Possibly cached connection in Directus | Restart the backend machine: `fly machine restart <id> --app gevoelscore-backend` |
