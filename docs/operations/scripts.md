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

29 fields checked across the 9 user collections plus the 2 M2M junctions (including provenance columns and the `tags.parent_id` self-FK). Exits 0 if all match, 1 if any mismatch.

**When to run**:

- Immediately after `setup-schema.mjs`
- After any schema change to verify nothing regressed
- During incident response when "the wrong data type" is a suspect

### [`directus/scripts/lib/tag-patterns.mjs`](../../directus/scripts/lib/tag-patterns.mjs)

Canonical tag-pattern map: ~80 candidate tags across the 6 v1 clusters, each with one-or-more regex patterns. Source of truth for note → tag matching. Exports `matchTags(note)` and `flatTagList()`. Shared by `analyze-notes.mjs`, `seed-tags.mjs`, and `import-real-history.mjs` — change this file, downstream scripts pick it up.

### [`directus/scripts/analyze-notes.mjs`](../../directus/scripts/analyze-notes.mjs)

Reads `private/real-history.csv` and reports tag-pattern frequencies + project-candidate date ranges + sample of unmatched notes (PII — console only, never written to disk). Pure read; safe to run any time. Use `--show-unmatched` for the unmatched sample.

### [`directus/scripts/seed-tags.mjs`](../../directus/scripts/seed-tags.mjs)

Idempotent: creates every tag in `lib/tag-patterns.mjs` in Directus. Re-running skips existing labels. When you add a new pattern to the lib, re-run this to add the corresponding tag.

### [`directus/scripts/seed-projects.mjs`](../../directus/scripts/seed-projects.mjs)

Idempotent: creates the 5 Project entities (Citalopram, CPAP, Naproxen, Breinvoeding, HeartMath) with their inferred date ranges. Edit the in-script `PROJECTS` array to add more.

### [`directus/scripts/import-real-history.mjs`](../../directus/scripts/import-real-history.mjs)

Imports `private/real-history.csv` (the user's 1.363-day Google Sheet) into Directus. Handles Dutch date format, quoted multi-column CSV cells, duplicate dates, future-prefilled blanks, and **populates the `tags` M2M relation** via the matched tag patterns. Defaults to dry-run; pass `--commit` to write. Idempotent upsert-by-date.

### [`directus/scripts/upgrade-m2m-tags.mjs`](../../directus/scripts/upgrade-m2m-tags.mjs)

**One-time migration** (2026-05-27): converted `day_entries.tag_ids` from a JSON-array field to a proper Directus M2M relation. The end state is now baked into `setup-schema.mjs`, so a fresh wipe-and-rebootstrap doesn't need this script. Kept in the repo as historical / reference.

### [`directus/scripts/add-tag-provenance.mjs`](../../directus/scripts/add-tag-provenance.mjs)

**One-time migration** (2026-05-27): adds `source` / `confidence` / `confirmed_at` columns to the `day_entries_tags` junction so we can distinguish user-chosen tags from regex-inferred ones. Backfills the existing 1,338 rows with `source='note_pattern', confidence=1.0` (since they all came from `import-real-history.mjs`). End state is baked into `setup-schema.mjs`. Kept as historical / reference.

### [`directus/scripts/flatten-day-entry-json-arrays.mjs`](../../directus/scripts/flatten-day-entry-json-arrays.mjs)

**One-time migration** (2026-05-27): drops the remaining JSON-array foreign-key fields (`day_entries.project_entry_ids`, `day_entries.calendar_event_ids`, `project_entries.tag_ids`) and upgrades `project_entries × tags` to a proper M2M junction. Has a pre-flight safety: refuses to drop a field that has non-empty data anywhere — safe to re-run on later instances where these fields might be populated. End state is baked into `setup-schema.mjs`. Kept as historical / reference.

### [`directus/scripts/add-tag-hierarchy.mjs`](../../directus/scripts/add-tag-hierarchy.mjs)

**One-time migration** (2026-05-27): adds the self-FK `tags.parent_id` so tags can form an intra-cluster hierarchy (e.g. `migraine.parent_id = hoofdpijn.id`, both in `fysiek`). `ON DELETE SET NULL` — children survive parent deletion. End state baked into `setup-schema.mjs`. Kept as historical / reference.

### [`directus/scripts/views/*.sql`](../../directus/scripts/views/)

Postgres views for cross-source querying. Three views:

- `daily_observations` — wide LEFT JOIN of day_entries × garmin_daily × health_daily × weather_daily by `date`. Most useful for v2.
- `day_tags_flat` — denormalised `(day, tag)` rows with provenance (`source`, `confidence`) for filtering.
- `tag_correlations` — pre-aggregated per-tag stats: `day_count`, `avg_score`, `stddev`, date range, `confirmed_day_count`.

All views use `CREATE OR REPLACE`, so re-applying after edits is idempotent. Apply with:

```powershell
psql $env:DB_CONNECTION_STRING -f directus/scripts/views/01-daily-observations.sql
psql $env:DB_CONNECTION_STRING -f directus/scripts/views/02-day-tags-flat.sql
psql $env:DB_CONNECTION_STRING -f directus/scripts/views/03-tag-correlations.sql
```

Or paste each file into the Neon SQL Editor in the Neon console. (Views live in Postgres directly; Directus is not involved unless you later register them as read-only collections in the admin UI.)

### [`directus/scripts/recompute-tag-usage.mjs`](../../directus/scripts/recompute-tag-usage.mjs)

Idempotent: counts junction rows per tag and updates `Tag.usage_count`. Directus doesn't auto-update the denormalized count. Run after any bulk import or significant tag-edit session.

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
