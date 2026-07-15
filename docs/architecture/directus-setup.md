# Directus + Fly.io setup runbook

Step-by-step setup instructions for the gevoelscore Directus instance and its Postgres backend (Neon at the time; self-hosted Fly Postgres since [ADR 0007](../decisions/0007-self-hosted-postgres-on-fly.md)). Implements [ADR 0003](../decisions/0003-directus-fly-infra-setup.md).

> **2026-07-14**: the Neon Postgres provisioning below is superseded by [ADR 0007](../decisions/0007-self-hosted-postgres-on-fly.md) (self-hosted Fly Postgres app `gevoelscore-pg`). It stands as historical record.

**Status of phases as of 2026-05-27:**

- ✅ **Phase 1 (provisioning)**: complete. Done in this session — backend app on Fly, Neon Postgres in EU, secrets staged, deployed. Directus serving at `https://gevoelscore-backend.fly.dev`.
- ⏳ **Phase 1.6 (admin login + 2FA)**: pending — needs you in the browser.
- ⏳ **Phase 2 (schema)**: pending — can be done either via admin UI clicks OR via Directus REST API once a static token exists (preferred — automatable).
- ⏳ **Phases 3–4 (roles, CORS)**: pending — same.
- ⏳ **Phase 5 (frontend)**: deferred until Next.js app exists.

---

## Prerequisites (you do once)

- Fly.io account with billing attached (~$5–10/month for this stack)
- `flyctl` CLI installed: `iwr https://fly.io/install.ps1 -useb | iex` (Windows) or `brew install flyctl` (macOS)
- `fly auth login` — confirm with `fly auth whoami`
- Cleared the gevoelscore-app folder is the working directory
- ADR 0003 read (or at least skimmed)

## Phase 1 — Provision the Directus backend

### 1.1 Create the Fly.io app

```powershell
cd gevoelscore-app/directus    # this folder doesn't exist yet — see Phase 1.2
fly apps create gevoelscore-backend --org personal
# Fallback if name taken: fly apps create gvscore-backend --org personal
```

### 1.2 Create the directus/ folder + fly.toml

Create `directus/fly.toml` in the gevoelscore-app repo. Copy from [ADR 0003 §Backend app](../decisions/0003-directus-fly-infra-setup.md#backend-app-gevoelscore-backend) — that block is verbatim ready.

Also create `directus/Dockerfile`:

```dockerfile
FROM directus/directus:11.17.2
# v11.17.2 matches the TVO instance for predictability. Bump when needed.
```

### 1.3 Provision Postgres (Neon, per [ADR 0003 amendment](../decisions/0003-directus-fly-infra-setup.md#amendment-2026-05-27-postgres-provider-switched-to-neon))

```powershell
# Auth to Neon (opens browser, click Authorize)
neonctl me

# Create the Neon project under the existing org
neonctl projects create `
  --name gevoelscore-db `
  --region-id aws-eu-central-1 `
  --org-id org-delicate-lake-28792527 `
  --output json | Out-File neon-create.json
# Grab `connection_uris[0].connection_parameters.pooler_host` and `password` from the JSON.
```

Build the **pooler** connection string (resilient to Neon scale-to-zero):

```
postgresql://neondb_owner:<password>@<pooler_host>/neondb?sslmode=require
```

Then attach it to Fly via secret (Phase 1.4).

### 1.4 Set bootstrap secrets

Generate two random 32-byte hex strings — these are Directus's `KEY` and `SECRET`. On Windows PowerShell:

```powershell
$key    = -join ((48..57) + (97..102) | Get-Random -Count 64 | ForEach-Object { [char]$_ })
$secret = -join ((48..57) + (97..102) | Get-Random -Count 64 | ForEach-Object { [char]$_ })

fly secrets set `
  KEY=$key `
  SECRET=$secret `
  ADMIN_EMAIL="you@example.com" `
  ADMIN_PASSWORD="<temporary, change immediately after first login>" `
  PUBLIC_URL="https://gevoelscore-backend.fly.dev" `
  CORS_ENABLED="true" `
  CORS_ORIGIN="https://gevoelscore-frontend.fly.dev" `
  CORS_CREDENTIALS="true" `
  DB_CLIENT="pg" `
  DB_CONNECTION_STRING="postgresql://neondb_owner:<password>@<pooler_host>/neondb?sslmode=require" `
  --app gevoelscore-backend
```

The temporary `ADMIN_PASSWORD` is used for the very first Directus login. **Change it from the Directus admin UI immediately**, then `fly secrets unset ADMIN_PASSWORD` so it doesn't linger in Fly's secret store.

### 1.5 Deploy

```powershell
fly deploy --app gevoelscore-backend
```

Wait for the deploy to finish (~2 minutes). Verify: `https://gevoelscore-backend.fly.dev/server/info` should return JSON with version `11.17.2`.

### 1.6 First admin login

Open `https://gevoelscore-backend.fly.dev/admin/`, log in with the bootstrap `ADMIN_EMAIL` + `ADMIN_PASSWORD`. Immediately:

1. **Change the admin password** in your user profile.
2. **Enable Two-Factor Authentication** on the admin user (Settings → Users → you → Two-Factor Authentication → Generate / Scan QR with authenticator app).
3. `fly secrets unset ADMIN_PASSWORD --app gevoelscore-backend` from your terminal — the password lives only in Directus's user table now.

---

## Phase 2 — Create the schema (Directus admin UI)

The data model is defined in [data-model.md](data-model.md). This phase translates every type there into a Directus collection. The order matters because of foreign keys: `tags` and `projects` first, then `day_entries`, then the rest.

### 2.1 Collection: `tags`

Settings → Data Model → Create Collection → `tags`.

| Field | Type | Settings |
|-------|------|----------|
| `id` | UUID | Primary key, auto-generated |
| `label` | String | Required, max 100 |
| `category` | Dropdown | Required. Choices: `mentaal`, `fysiek`, `overall`, `activiteit`, `gebeurtenis`, `interventie`, `project`, `custom`. (Locked enum — see [data-model.md "Tag"](data-model.md).) |
| `project_id` | UUID | Nullable. FK → `projects.id` (set up after `projects` collection exists). |
| `usage_count` | Integer | Required, default `0`, min `0` |
| `archived_at` | Timestamp | Nullable |
| `created_at` | Timestamp | Auto-set on create |

After creation, the seed tags from REQUIREMENTS.md are inserted by the import step or via admin UI bulk-insert.

### 2.2 Collection: `projects` (v1.5 — empty in v1)

Schema exists from day 1 per [data-model.md "Schema-readiness rule"](data-model.md#schema-readiness-rule).

| Field | Type | Settings |
|-------|------|----------|
| `id` | UUID | Primary key |
| `name` | String | Required, max 200 |
| `type` | Dropdown | Choices: `medicatie`, `therapie`, `oefening`, `anders` |
| `start_date` | Date | Required |
| `end_date` | Date | Nullable |
| `status` | Dropdown | Choices: `active`, `paused`, `completed`, `archived`. Default `active`. |
| `description` | Text | Nullable |
| `created_at`, `updated_at` | Timestamp | Auto |

Then back to `tags`: set up the `project_id` FK → `projects.id`.

### 2.3 Collection: `project_field_configs` (v1.5 — empty in v1)

| Field | Type | Settings |
|-------|------|----------|
| `id` | UUID | Primary key |
| `project_id` | UUID | FK → `projects.id`, required |
| `key` | String | Required, max 50 |
| `label` | String | Required, max 100 |
| `type` | Dropdown | Choices: `text`, `tag_set`, `number` |
| `unit` | String | Nullable, max 20 |
| `default_visible` | Boolean | Default `true` |

### 2.4 Collection: `day_entries`

The cardinal entity. Every field per the [data-model.md DayEntry type](data-model.md#dayentry).

| Field | Type | Settings |
|-------|------|----------|
| `id` | UUID | Primary key |
| `date` | Date | **UNIQUE**, required. Natural key. |
| `score` | Integer | Required, min 1, max 10 |
| `note` | Text | Nullable |
| `tag_ids` | M2M to `tags` (via Directus-generated junction `day_entries_tags`) | Empty by default |
| `sub_scores` | JSON | Nullable. Shape `{ cognitive, physical, mental }` each 1–6 or null. Empty in v1. |
| `sleep_hours` | Float | Nullable. 0–24. Empty in v1. |
| `special_event` | String | Nullable. v1.5. |
| `project_entry_ids` | M2M to `project_entries` | Empty in v1. |
| `calendar_event_ids` | M2M to `calendar_events` | Empty in v1. |
| `garmin` | JSON | Nullable. v2. |
| `health` | JSON | Nullable. v2. |
| `weather` | JSON | Nullable. v2. |
| `derived` | JSON | Nullable. v2. |
| `created_at`, `updated_at` | Timestamp | Auto |

The M2M junction `day_entries_tags` is auto-created by Directus when you add the M2M relation.

### 2.5 Collection: `project_entries` (v1.5 — empty in v1)

| Field | Type | Settings |
|-------|------|----------|
| `id` | UUID | Primary key |
| `date` | Date | Required. Composite UNIQUE with `project_id`. |
| `project_id` | UUID | FK → `projects.id`, required |
| `note` | Text | Nullable |
| `tag_ids` | M2M → `tags` | |
| `numeric_values` | JSON | Shape `{ [field_key]: number }`. Nullable. |
| `created_at`, `updated_at` | Timestamp | Auto |

UNIQUE constraint on `(date, project_id)` per [data-model.md ID strategy](data-model.md#id-strategy).

### 2.6 Collection: `calendar_events` (v1.5 — empty in v1)

| Field | Type | Settings |
|-------|------|----------|
| `id` | UUID | Primary key |
| `google_event_id` | String | **UNIQUE**, required (stable Google event ID) |
| `date` | Date | Required |
| `title` | String | Required |
| `start_time` | Timestamp | Nullable |
| `end_time` | Timestamp | Nullable |
| `all_day` | Boolean | Default `false` |
| `calendar_source` | String | Required |
| `attendees_count` | Integer | Nullable |
| `location` | String | Nullable |
| `relevance` | Dropdown | Choices: `high`, `normal`, `hidden`. Default `normal`. |
| `category_hint` | String | Nullable |

### 2.7 Empty placeholder collections (v2 — schema exists, no rows in v1)

Per [data-model.md "Schema-readiness rule"](data-model.md#schema-readiness-rule), these collections are created in v1 even though never written to:

- `garmin_daily` — fields per [technisch_document.md "GarminDaily"](../technisch_document.md). Add `date` (UNIQUE), and JSON columns for the aggregate fields.
- `health_daily` — fields per [technisch_document.md HealthKit section](../technisch_document.md).
- `weather_daily` — fields per [technisch_document.md "WeatherDaily"](../technisch_document.md).

Create them with minimum field sets (just `id`, `date` UNIQUE, and a `data` JSON column) for v1. Refine when v2 work begins.

---

## Phase 3 — Roles & permissions (Directus admin UI)

### 3.1 The frontend's role: `gevoelscore-frontend-api`

Settings → Access Control → Create Role → `gevoelscore-frontend-api`.

This role is what the Next.js frontend uses (via Directus auth). It has narrow CRUD on the collections it needs:

| Collection | Permissions |
|-----------|-------------|
| `day_entries` | Full CRUD (all rows — single-user app, all rows belong to you) |
| `day_entries_tags` (junction) | Full CRUD |
| `tags` | Full CRUD |
| `projects` | Full CRUD (v1.5 — but role exists in v1 so the schema is stable) |
| `project_entries` | Full CRUD (v1.5) |
| `project_field_configs` | Full CRUD (v1.5) |
| `calendar_events` | Full CRUD (v1.5) |
| `garmin_daily`, `health_daily`, `weather_daily` | None in v1 (the future native iOS app gets its own role when v2 lands) |
| All Directus system collections (`directus_users`, etc.) | **None** — the frontend has no business reading the user table |

### 3.2 Public role: deny everything

Settings → Access Control → Public → ensure **no read access** to any user collection. This is the default but verify it. Per [.claude/security-checklist.md](../../.claude/security-checklist.md#a01--broken-access-control) — no anonymous reads.

### 3.3 Your admin user

Already exists from Phase 1.6. Keep it as `Administrator` role. It's the recovery account.

---

## Phase 4 — CORS hardening

Settings → Project Settings → CORS section:

- **CORS Enabled**: yes
- **CORS Origin**: `https://gevoelscore-frontend.fly.dev` (exact, no wildcards)
- **CORS Methods**: `GET, POST, PATCH, DELETE, OPTIONS`
- **CORS Allowed Headers**: default + `X-CSRF-Token` (only if we end up using the double-submit pattern; per [security-checklist](../../.claude/security-checklist.md#a08--data-integrity-csrf) the current design is `SameSite=Strict` + Origin check, which doesn't need this header)
- **CORS Credentials**: `true` — required for `httpOnly` cookie auth

These also map to the env vars set in Phase 1.4 (`CORS_ENABLED`, `CORS_ORIGIN`, `CORS_CREDENTIALS`).

---

## Phase 5 — Provision the frontend

### 5.1 Create the Fly.io app

```powershell
fly apps create gevoelscore-frontend --org personal
```

### 5.2 Create the Next.js app folder + fly.toml + Dockerfile

The Next.js project itself doesn't exist yet — that's a separate feature plan. When it does, drop `fly.toml` per [ADR 0003 §Frontend app](../decisions/0003-directus-fly-infra-setup.md#frontend-app-gevoelscore-frontend) and a standard Next.js Dockerfile in the project root.

### 5.3 Deploy

```powershell
fly deploy --app gevoelscore-frontend
```

The frontend will fail to authenticate against Directus until the `gevoelscore-frontend-api` role has at least one user assigned. That's the next feature: login flow.

---

## Phase 6 — Verification checklist

Once everything is deployed:

- [ ] `https://gevoelscore-backend.fly.dev/server/info` returns Directus 11.17.2 JSON
- [ ] `https://gevoelscore-backend.fly.dev/admin/` loads the Directus admin UI
- [ ] Admin user has 2FA enabled (try logging out + back in — should prompt for TOTP)
- [ ] `ADMIN_PASSWORD` is no longer in `fly secrets list --app gevoelscore-backend`
- [ ] CORS: from any origin other than the frontend, a `fetch` to the backend should fail at the preflight (test in browser DevTools: `await fetch('https://gevoelscore-backend.fly.dev/items/day_entries')` from a different origin should be blocked)
- [ ] The 7 v1 collections exist, with correct types and constraints (UNIQUE on `day_entries.date`, etc.)
- [ ] The 3 empty placeholder collections exist (v2 — schema-readiness rule)
- [ ] `gevoelscore-frontend-api` role has the permissions table from Phase 3.1
- [ ] Public role has no read access on any collection
- [ ] `https://gevoelscore-frontend.fly.dev` loads (placeholder page is fine for now — login feature delivers real content)

If any item fails, fix before moving on. Treat the verification list as a single transaction.

---

## What's NOT in this runbook (deferred)

- Custom domain (`fly certs add`) — v1.5 polish
- CI/CD automation — manual `fly deploy` is fine for v1's solo-dev pace
- Programmatic schema apply via `npx directus schema apply` — the JSON snapshot is in Directus admin UI for the first cut; export it as `schema-snapshot.json` later if regen-from-scratch becomes a need
- Email transport (Brevo, SES) — v1 has no email flows
- Storage adapter for uploads — v1 has no uploads; default local mount is fine

---

## When the runbook fails

If a step doesn't work:

1. **Compare to TVO**: `programmeerprobeer/directus/fly.toml`, `programmeerprobeer/tvoo_frontend/fly.toml`, and any `programmeerprobeer/docs/security/` references for the shape of working config.
2. **Check Fly logs**: `fly logs --app gevoelscore-backend` (or `--app gevoelscore-frontend`). Most issues surface here.
3. **Check Directus logs**: same `fly logs` command. Directus's own startup errors are usually about missing env vars or bad CORS config.
4. **Rollback path**: `fly apps destroy gevoelscore-backend --yes` (and `gevoelscore-frontend`, `gevoelscore-db`) wipes everything. Costs nothing because Fly bills per machine-second.
