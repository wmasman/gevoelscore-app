# Current deployed state

**Living document — update on every infrastructure change.**

**Last updated**: 2026-05-27 (initial infra deployment + sample data imported)

---

## Cloud resources

### Fly.io (org: `personal`, slug: `wmas`)

| App | Region | Status | URL | Resources |
|-----|--------|--------|-----|-----------|
| `gevoelscore-backend` | `ams` | ✅ deployed, running | https://gevoelscore-backend.fly.dev | 1 GB RAM, 1 shared CPU, Directus 11.17.2 |
| `gevoelscore-frontend` | `ams` | ⏳ app slot only, no deploy | https://gevoelscore-frontend.fly.dev | Next.js Dockerfile + fly.toml not yet written |

**Backend secrets** (set via `fly secrets`, never committed):

| Name | Purpose |
|------|---------|
| `KEY` | Directus encryption key (32-byte hex). Generated at provisioning; rotate only if compromised. |
| `SECRET` | Directus auth secret (32-byte hex). Same lifecycle as `KEY`. |
| `DB_CLIENT` | Always `pg`. |
| `DB_CONNECTION_STRING` | Pooled Neon connection URI with embedded password. Rotate when the Neon password rotates. |
| `PUBLIC_URL` | `https://gevoelscore-backend.fly.dev`. |
| `CORS_ENABLED` | `true`. |
| `CORS_ORIGIN` | `https://gevoelscore-frontend.fly.dev` — exact match, no wildcards. |
| `CORS_CREDENTIALS` | `true` — required for `httpOnly` cookie auth from the frontend. |
| `ADMIN_EMAIL` | `wmasman@gmail.com` — the bootstrap admin user. |
| `ADMIN_PASSWORD` | ⚠️ **Should be unset.** Set during bootstrap, used only for the first admin login. Remove via `fly secrets unset ADMIN_PASSWORD --app gevoelscore-backend` once you've changed it in the Directus admin UI. |

**Volumes:**

| Name | Mount | Size | Notes |
|------|-------|------|-------|
| `gevoelscore_uploads` | `/directus/uploads` (in backend container) | 1 GB | Encrypted, automatic snapshots. Empty in v1 (no file uploads yet). |

### Neon (org: `tvo-backend-database`, slug: `org-delicate-lake-28792527`)

| Project | Region | Database | Postgres | Branches |
|---------|--------|----------|----------|----------|
| `gevoelscore-db` | `aws-eu-central-1` | `neondb` | 17 | `main` (production branch only — no staging branch yet) |

**Endpoints:**

- Direct: `ep-flat-grass-alwa40oq.c-3.eu-central-1.aws.neon.tech`
- Pooler: `ep-flat-grass-alwa40oq-pooler.c-3.eu-central-1.aws.neon.tech` ← **used by Directus** (resilient to scale-to-zero)

**Role:** `neondb_owner` — used by Directus. Auto-created by Neon at project provisioning.

---

## Directus state

### Collections (9 user collections)

| Collection | Purpose | Status | v1 use |
|-----------|---------|--------|--------|
| `day_entries` | The cardinal entity — one row per local-date logged | ✅ created (60 sample rows imported 2026-05-27) | **YES** — daily entries |
| `tags` | Personal/dynamic tag set (5 clusters + interventie/project/custom) | ✅ created | **YES** — tag chips |
| `projects` | Active interventions/projects (Citalopram, Breinvoeding, etc.) | ✅ created | No — v1.5 |
| `project_field_configs` | Per-project field definitions | ✅ created | No — v1.5 |
| `project_entries` | Per-project per-day entries | ✅ created | No — v1.5 |
| `calendar_events` | Google Calendar read-only sync | ✅ created | No — v1.5 |
| `garmin_daily` | Garmin aggregate per day | ✅ placeholder | No — v2 (separate native iOS app) |
| `health_daily` | Apple Health aggregate per day | ✅ placeholder | No — v2 |
| `weather_daily` | Weather per location per day | ✅ placeholder | No — v2 |

**Schema verification**: all 21 critical PostgreSQL type checks pass — see [`directus/scripts/verify-schema.mjs`](../../directus/scripts/verify-schema.mjs). No silent VARCHAR-where-INTEGER bugs.

**M2M deferral**: `day_entries.tag_ids`, `day_entries.project_entry_ids`, `day_entries.calendar_event_ids` are JSON arrays of UUIDs in v1. Migrating to proper M2M junctions is v1.5 work; the domain layer's `tag_ids: string[]` contract survives either representation.

### Auth

| ID | Type | Name | Purpose |
|----|------|------|---------|
| `16f6f68b-e683-4dc9-8afc-e80695c4259d` | User | wmasman@gmail.com | Admin recovery user. 2FA enabled. |
| `fdf942a5-b552-4c48-a04b-7d20f560ff4c` | Role | `gevoelscore-frontend-api` | What the Next.js frontend's Directus user will be assigned. No user assigned yet — that's a manual admin-UI step when wiring up the frontend. |
| `2ba264ec-12e6-49c4-929a-6babe3a441e2` | Policy | `gevoelscore-frontend-policy` | Linked to the role above. Holds the 24 permission entries (6 collections × CRUD). |

### Permissions on `gevoelscore-frontend-policy`

| Collection | Actions granted | Filter |
|-----------|----------------|--------|
| `day_entries` | create, read, update, delete | all rows (`{}`) |
| `tags` | create, read, update, delete | all rows |
| `projects` | create, read, update, delete | all rows |
| `project_entries` | create, read, update, delete | all rows |
| `project_field_configs` | create, read, update, delete | all rows |
| `calendar_events` | create, read, update, delete | all rows |
| `garmin_daily`, `health_daily`, `weather_daily` | **none** | v2 native iOS app territory |
| `directus_users`, `directus_roles`, etc. | **none** | admin-only |

Public role has no read access anywhere. No anonymous data access.

---

## Local repository state

### `directus/` folder

```
directus/
├── Dockerfile           — FROM directus/directus:11.17.2
├── fly.toml             — Fly app config for gevoelscore-backend
├── .dockerignore
├── .env.example         — Env var template for the scripts (DIRECTUS_TOKEN, DIRECTUS_URL)
└── scripts/
    ├── lib/
    │   └── directus-request.mjs  — Shared auth + fetch helper
    ├── setup-schema.mjs          — Creates the 9 collections (idempotent, one-POST rule)
    ├── verify-schema.mjs         — Confirms PostgreSQL types match expectations
    └── setup-permissions.mjs     — Creates role + policy + 24 permissions (idempotent)
```

### Code (`src/`)

| Module | Tests | Status |
|--------|-------|--------|
| `src/lib/domain/score.ts` | 26 | ✅ shipped |
| `src/lib/domain/date.ts` | 25 | ✅ shipped |
| `src/lib/domain/note.ts` | 11 | ✅ shipped |
| `src/lib/domain/tag-ids.ts` | 19 | ✅ shipped |
| `src/lib/domain/sub-score.ts` | 30 | ✅ shipped |
| `src/lib/domain/sleep-hours.ts` | 14 | ✅ shipped |
| `src/lib/domain/day-entry.ts` | 24 | ✅ shipped |
| `src/lib/domain/tag-label.ts` | 14 | ✅ shipped |
| `src/lib/domain/tag-category.ts` | 19 | ✅ shipped |
| `src/lib/domain/tag.ts` | 30 | ✅ shipped |
| `src/lib/import/csv-day-entries.ts` | 22 | ✅ shipped — parser only, not yet wired to Directus |
| `src/app/*` (Next.js) | 0 | ❌ not started |

**Test suite**: 254/254 passing, typecheck clean, `npm audit` clean.

---

## What's NOT yet done

In the order they should be tackled:

1. **Create the frontend-app Directus user** (5 min in admin UI)
   - Settings → Access Control → Users → Create
   - Assign role `gevoelscore-frontend-api`
   - Set a password (random, store in password manager)
   - Enable 2FA
2. **Bootstrap Next.js** in this repo (one terminal session, ~20 min)
   - `pnpm create next-app gevoelscore-frontend --typescript --app --tailwind --eslint`
   - Adapt the resulting `src/app/` to share the existing `src/lib/domain/` types
   - Add Dockerfile + reuse the existing `fly.toml` from [ADR 0003](../decisions/0003-directus-fly-infra-setup.md) (or apply the runbook commands)
3. **Implement login feature** ([docs/features/login/](../features/login/) has the plan)
4. **Implement daily-entry screen** (the cardinal-principle UI work)
5. **Wire the CSV import to Directus** (parser is done; needs upsert glue)
6. **Implement recent-missed-days, calendar, timeline, settings** in order

---

## Maintenance reminders

- **Directus version**: 11.17.2 (one behind 11.17.4). Bump on security advisories. Test on staging first when you set up a staging branch.
- **Neon free-tier limits**: 3 branches, 0.5 GB storage. Not close to either.
- **Fly bills**: check ~$5–7/mo. If it spikes, run `fly machine list --app gevoelscore-backend` and `fly volumes list` to see what's running.
- **Backup verification**: Neon takes daily snapshots automatically. Once a quarter, test a restore (`neonctl branches create --parent main` makes a copy you can poke at without touching production).
