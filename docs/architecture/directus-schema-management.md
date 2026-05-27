# Directus schema management

Canonical approach for managing the Directus schema in the gevoelscore project, distilled from the TVO/programmeerprobeer codebase (which has been through this twice and has the scars to prove it).

---

## TL;DR

- **Bootstrap (one-time)**: handled automatically by Directus's own startup migrations the first time it connects to an empty Postgres database. **Already done** for gevoelscore as of 2026-05-27.
- **Schema creation (this project's authoritative path)**: write idempotent Node.js scripts that hit the Directus REST API with a static admin token. Each script creates **one collection + all its fields in a single POST** (this is critical — see "The one-POST rule" below).
- **Schema changes (ongoing)**: small new collections / fields → write a new idempotent script and run it. Bigger changes that involve data movement → write a one-shot migration script with progress tracking.
- **Roles + permissions**: same pattern — REST API, idempotent, scripted.
- **CORS**: env vars on Fly (`CORS_ENABLED`, `CORS_ORIGIN`, `CORS_CREDENTIALS`). Already set.

Schema-as-code lives in `directus/scripts/*.mjs`. Snapshots (`schema.yml`) are NOT used — they were tried in the TVO project and abandoned because `schema apply` can't bootstrap empty DBs and gets messy with renames.

---

## What we learned from programmeerprobeer

Three lessons that cost the TVO project real time to learn. Captured here so gevoelscore doesn't re-learn them.

### Lesson 1: `npx directus bootstrap` is one-time only

`bootstrap` creates the `directus_*` system tables in an empty Postgres database. If you put it in your container's startup script, **the server hangs on every restart** (the bootstrap process doesn't exit properly when there's nothing to do).

**What we do**: Directus 11 auto-runs its own migrations when it connects to a DB. No explicit `bootstrap` step needed for us. If we ever wipe the DB and start fresh, deploy once with bootstrap in the startup, then redeploy without it. (TVO learned this the hard way; we won't repeat it.)

### Lesson 2: `schema apply` cannot bootstrap empty databases

```
ERROR: Cannot read properties of undefined (reading 'find')
  at getSnapshotDiff (...)
```

The CLI command requires `directus_collections` metadata to exist. It's a *diff-and-sync* tool for existing schemas, not a *create-from-scratch* tool.

**What we do**: skip `schema apply` entirely. Use REST API scripts. They work on any state (empty, partial, fully populated) thanks to idempotent guards.

### Lesson 3: The one-POST rule — **THIS IS THE BIG ONE**

When creating a collection via REST API, **always include all fields in the same POST request** as the collection itself. **Never** create the collection bare and then add fields one-by-one.

**Wrong** — produces broken PostgreSQL types (VARCHAR where INTEGER was specified, etc.):

```javascript
await fetch(`${URL}/collections`, { method: 'POST', body: JSON.stringify({ collection: 'my_table' }) });
await fetch(`${URL}/fields/my_table`, { method: 'POST', body: JSON.stringify({ field: 'foo', type: 'integer' }) });
await fetch(`${URL}/fields/my_table`, { method: 'POST', body: JSON.stringify({ field: 'bar', type: 'string' }) });
// Result: Directus API reports "type: integer" but PostgreSQL column is VARCHAR.
//         Migrations fail silently for any value > the VARCHAR length.
```

**Right** — Directus translates types correctly when given full context up front:

```javascript
await fetch(`${URL}/collections`, {
  method: 'POST',
  body: JSON.stringify({
    collection: 'my_table',
    schema: { name: 'my_table' },
    fields: [
      { field: 'id', type: 'uuid', schema: { is_primary_key: true } },
      { field: 'foo', type: 'integer', schema: { is_nullable: false } },
      { field: 'bar', type: 'string', schema: { is_nullable: false } },
    ],
  }),
});
```

**Why this matters for us**: every collection in our data model (day_entries, tags, etc.) has multiple fields with specific types. If we get the one-POST rule wrong on `day_entries.score`, we'd end up with a VARCHAR column when we needed INTEGER, and our 1–10 validation would still pass the domain layer but rows with `score: 10` might silently get stored as the string `"10"`. Catch this at creation time, not at row 227 of the import.

**Mitigation**: every script calls a `verifyFieldType()` helper after creation that confirms the actual PostgreSQL `data_type` matches expectations. Mismatch → loud failure.

---

## Script conventions (mirroring `programmeerprobeer/directus/scripts/`)

Every script in `directus/scripts/` follows the same shape:

1. **Reads config from env vars** — `DIRECTUS_URL` defaults to `https://gevoelscore-backend.fly.dev`; `DIRECTUS_TOKEN` is the static admin token (set as a local env var, never committed).
2. **Has an `authenticate()` or `setToken()` helper** that pulls from env.
3. **Wraps `fetch()` in a `directusRequest()` helper** that adds the Bearer header, handles 204s, throws on non-2xx with the error body.
4. **Is idempotent** — checks if the collection/field/role already exists before creating. Re-running the script is always safe.
5. **Validates schema after each create** — calls `verifyFieldType()` to confirm PostgreSQL type matches the Directus type.
6. **Has a top banner** logging which env it's hitting (so you don't accidentally hit production while developing).

Template lives at the top of `setup-schema.mjs` (next file to write).

---

## Why no Zod migrations / Prisma / Drizzle?

Tempting alternative: define the schema in TypeScript (Zod, Prisma, Drizzle), generate migrations, apply them. We don't do this because:

- **Directus owns the schema.** It writes `directus_collections`, `directus_fields`, and `directus_relations` metadata that's tightly coupled to the underlying tables. An external migration tool that bypasses this metadata leaves Directus's admin UI in an inconsistent state.
- **The domain types (`src/lib/domain/`) are already the single source of truth for application validation.** They run in the browser, in API routes, and in import scripts — wherever data crosses a boundary. Directus's schema just needs to be *compatible* with those types, not a copy of them.
- **One layer to keep in sync, not two.** Schema lives in Directus + scripts in `directus/scripts/`; validation lives in `src/lib/domain/`. Each has a clear owner.

---

## File layout

```
gevoelscore-app/
  directus/
    Dockerfile                       — FROM directus/directus:11.17.2
    fly.toml                         — Fly app config (deployed)
    .dockerignore
    scripts/
      setup-schema.mjs               — Creates the 7 v1 + 3 v2-placeholder collections, idempotent
      setup-permissions.mjs          — Creates role + permissions, idempotent
      verify-schema.mjs              — Sanity-checks every collection's PostgreSQL types match expectations
      lib/
        directus-request.mjs         — Shared fetch wrapper (auth, error handling)
        verify-field-type.mjs        — Post-create PostgreSQL type guard
  src/lib/domain/                    — Application validators (separate, already shipped)
  docs/architecture/
    directus-setup.md                — Provisioning runbook
    directus-schema-management.md    — This document
    data-model.md                    — The single source of truth for what fields exist
```

---

## Recovery / wipe procedures

If the schema ever gets into a bad state (mismatched types, orphan fields, broken FKs):

### Option A — surgical fix

Use the admin UI to delete the broken field/collection. Re-run the relevant `setup-*.mjs` script. The idempotent guards re-create cleanly.

### Option B — full wipe

```bash
# 1. Drop the Neon DB (via neon UI or `neonctl databases delete neondb && create`)
# 2. Restart the backend so Directus auto-bootstraps on the empty DB
fly machine restart --app gevoelscore-backend

# 3. Re-run all setup scripts
node directus/scripts/setup-schema.mjs
node directus/scripts/setup-permissions.mjs
node directus/scripts/verify-schema.mjs

# 4. Re-import historical data from the CSV
node directus/scripts/import-historical-data.mjs   # (not yet written; comes with the daily-entry feature)
```

**Don't drop the entire Neon project** unless you also want to lose the project ID — that ID is in fly secrets and changing it means re-deploying. Wipe the database, not the project.

---

## References

- [migration-best-practices.md (programmeerprobeer)](../../../programmeerprobeer/directus/docs/migration-best-practices.md) — the canonical reference; the one-POST rule and the schema-verification pattern come from here.
- [migration-flow.md (programmeerprobeer)](../../../programmeerprobeer/directus/docs/migration-flow.md) — the actual TVO migration story; pattern reuse for import flows.
- [SCHEMA_BOOTSTRAP_SOLUTION.md (programmeerprobeer)](../../../programmeerprobeer/directus/SCHEMA_BOOTSTRAP_SOLUTION.md) — the cautionary tale about `schema apply` and the bootstrap loop. Read this if anything goes weird.
- [directus-v11-bootstrap-guide.md (programmeerprobeer)](../../../programmeerprobeer/directus/docs/directus-v11-bootstrap-guide.md) — quick reference for the bootstrap commands.
- [data-model.md](data-model.md) — the gevoelscore-specific source of truth for what collections we need.
- [Directus API docs](https://directus.io/docs/api) — official.
