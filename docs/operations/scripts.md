# Scripts inventory

What lives in `directus/scripts/` and how to run it.

All scripts:

- Use Node 18+ built-in `fetch` (no `node_modules` in `directus/`).
- Read config from `DIRECTUS_URL` (default `https://gevoelscore-backend.fly.dev`) and `DIRECTUS_TOKEN` (required) env vars.
- Are **idempotent** — re-running is safe; the safety guards skip already-existing objects.

---

## Running a script

```powershell
# Get a static token: Directus admin UI → User Profile → Token → Generate
$env:DIRECTUS_TOKEN = "<your token>"

node directus/scripts/setup-schema.mjs
node directus/scripts/verify-schema.mjs
node directus/scripts/setup-permissions.mjs
```

Or, with a `.env.local` file (gitignored):

```powershell
# directus/.env.local
DIRECTUS_TOKEN=<your token>
DIRECTUS_URL=https://gevoelscore-backend.fly.dev
```

Then load it before running (no automatic loading — keeps the script dep-free):

```powershell
Get-Content directus/.env.local | ForEach-Object {
  $name, $value = $_.split('=', 2)
  if ($name -and $value) { Set-Item "env:$name" $value }
}

node directus/scripts/setup-schema.mjs
```

---

## Script catalogue

### [`directus/scripts/lib/directus-request.mjs`](../../directus/scripts/lib/directus-request.mjs)

Shared helpers:

- `directusRequest(endpoint, method, body)` — fetch wrapper with auth + error handling.
- `collectionExists(name)` — true if a Directus user-collection exists.
- `getField(collection, field)` — returns the field metadata + actual PostgreSQL type.
- `banner(name)` — top-of-script banner showing which env you're hitting.

Imported by the other scripts. Not directly executed.

### [`directus/scripts/setup-schema.mjs`](../../directus/scripts/setup-schema.mjs)

Creates the 9 user collections (`day_entries`, `tags`, `projects`, `project_entries`, `project_field_configs`, `calendar_events`, `garmin_daily`, `health_daily`, `weather_daily`) in dependency order.

**Strict invariant** (the one-POST rule, see [architecture/directus-schema-management.md](../architecture/directus-schema-management.md)): each collection is created with **all its fields in one POST**. Never `POST /collections` and then `POST /fields/...` separately — that produces silent VARCHAR-where-INTEGER bugs.

**Idempotency**: each collection check happens via `collectionExists()`. Re-running prints `⏩ already exists` for each and finishes in ~1 second.

**When to run**:

- Initial setup (already done 2026-05-27)
- After [wipe-and-rebootstrap](runbooks/wipe-and-rebootstrap.md)
- If you add a new collection to the script and want to apply it (just re-run — existing collections are skipped)

### [`directus/scripts/verify-schema.mjs`](../../directus/scripts/verify-schema.mjs)

Confirms that the PostgreSQL `data_type` of every critical field matches the Directus `type` you asked for. Catches silent translation bugs.

21 fields checked across the 9 collections. Exits 0 if all match, 1 if any mismatch.

**When to run**:

- Immediately after `setup-schema.mjs`
- After any schema change to verify nothing regressed
- During incident response when "the wrong data type" is a suspect

### [`directus/scripts/import-sample-data.mjs`](../../directus/scripts/import-sample-data.mjs)

Imports the anonymized 60-day sample at [`docs/sample-data.csv`](../sample-data.csv) into the live `day_entries` collection. **Idempotent**: upsert by date — re-running PATCHes existing rows, POSTs new ones.

Uses a deliberately minimal inline CSV parser (sample is 2-column, simple quoted). The canonical 3-column parser at [`src/lib/import/csv-day-entries.ts`](../../src/lib/import/csv-day-entries.ts) is reserved for the user-facing import flow that ships with the daily-entry feature (will run inside Next.js where TS is native).

**When to run**:
- After initial Directus setup, to validate the full stack (CSV → domain validation → REST → Neon) end-to-end before any UI work.
- After [wipe-and-rebootstrap](runbooks/wipe-and-rebootstrap.md), to re-seed.
- Whenever you want a known-state test dataset for screen development.

### [`directus/scripts/setup-permissions.mjs`](../../directus/scripts/setup-permissions.mjs)

Creates (idempotently) the chain:

```
Role "gevoelscore-frontend-api"
  ├─ linked via directus_access
  └─ Policy "gevoelscore-frontend-policy"
        ├─ create | read | update | delete on day_entries
        ├─ create | read | update | delete on tags
        ├─ create | read | update | delete on projects
        ├─ create | read | update | delete on project_entries
        ├─ create | read | update | delete on project_field_configs
        └─ create | read | update | delete on calendar_events
```

Permissions on `garmin_daily`, `health_daily`, `weather_daily` are NOT granted (v2 native iOS app territory). Permissions on `directus_*` system collections are NOT granted (admin-only).

**When to run**:

- Initial setup (already done 2026-05-27)
- After wipe-and-rebootstrap
- If the data model adds new collections (add them to `FRONTEND_CRUD_COLLECTIONS` in the script)

---

## What scripts NOT to write

Anti-patterns from the programmeerprobeer history:

1. **Don't write a script that calls `npx directus bootstrap` on every container start.** Bootstrap hangs the server on subsequent restarts. Bootstrap is one-time only; Directus 11 auto-runs migrations on its own.
2. **Don't use `npx directus schema apply` to create a schema from scratch.** It requires existing `directus_collections` metadata; fails on empty databases with a confusing "Cannot read properties of undefined" error.
3. **Don't write a script that creates a collection bare, then adds fields one by one.** This is the silent-VARCHAR-bug pattern. Always include all fields in the same POST as the collection.

See [`docs/architecture/directus-schema-management.md`](../architecture/directus-schema-management.md) for the full rationale.

---

## Future scripts to add (when needed)

| Script | Purpose | When to write |
|--------|---------|---------------|
| `setup-seed-tags.mjs` | Insert the 25–30 seed tags (mentaal/fysiek/overall/activiteit/gebeurtenis) on a fresh install | When you want one-tap-friendly tag chips on the daily screen from day 1 |
| `import-historical-csv.mjs` | Wraps [`src/lib/import/csv-day-entries.ts`](../../src/lib/import/csv-day-entries.ts), upserts parsed rows into Directus | When the CSV import feature ships |
| `rotate-db-password.mjs` | Automate the Neon password rotation steps in [rotate-credentials.md](runbooks/rotate-credentials.md) | If rotation becomes routine (i.e., a schedule, not just incident-response) |
| `backup-snapshot.mjs` | `neonctl branches create --parent main --name backup-YYYY-MM-DD` for manual snapshot before risky migrations | First time you do a destructive schema change |
