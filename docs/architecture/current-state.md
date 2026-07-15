# Current deployed state

**Living document — update on every infrastructure change.**

**Last updated**: 2026-07-14 (database migrated from Neon to self-hosted Fly Postgres `gevoelscore-pg`, per [ADR 0007](../decisions/0007-self-hosted-postgres-on-fly.md)). Previous update 2026-05-28: daily-entry feature Steps 0–6 + 4b **deployed to Fly** at commit `58a3667`; live at https://gevoelscore-frontend.fly.dev; app installed as iOS PWA by the single user — feature is in real-usage soak.

---

## Cloud resources

### Fly.io (org: `personal`, slug: `wmas`)

| App | Region | Status | URL | Resources |
|-----|--------|--------|-----|-----------|
| `gevoelscore-backend` | `ams` | ✅ deployed, running | https://gevoelscore-backend.fly.dev | 1 GB RAM, 1 shared CPU, Directus 11.17.2 |
| `gevoelscore-frontend` | `ams` | ✅ deployed, running (1 machine) | https://gevoelscore-frontend.fly.dev | Next.js 15.5 + Tailwind v4 + login + daily-entry (score row, note, tag picker, timeline w/ bottom sheet). Warm-earth design tokens. Image ~65 MB (standalone build). Scaled to 1 machine (matches in-memory session/rate-limit assumption per ADR 0003). |

**Backend secrets** (set via `fly secrets`, never committed):

| Name | Purpose |
|------|---------|
| `KEY` | Directus encryption key (32-byte hex). Generated at provisioning; rotate only if compromised. |
| `SECRET` | Directus auth secret (32-byte hex). Same lifecycle as `KEY`. |
| `DB_CLIENT` | Always `pg`. |
| `DB_CONNECTION_STRING` | Fly Postgres flycast URI (`postgres://postgres:<password>@gevoelscore-pg.flycast:5432/gevoelscore`) with embedded password. Rotate per [runbooks/rotate-credentials.md](../operations/runbooks/rotate-credentials.md). |
| `PUBLIC_URL` | `https://gevoelscore-backend.fly.dev`. |
| `CORS_ENABLED` | `true`. |
| `CORS_ORIGIN` | `https://gevoelscore-frontend.fly.dev` — exact match, no wildcards. |
| `CORS_CREDENTIALS` | `true` — required for `httpOnly` cookie auth from the frontend. |
| `ADMIN_EMAIL` | The bootstrap admin user's email (stored in 1Password). |
| `ADMIN_PASSWORD` | ⚠️ **Should be unset.** Set during bootstrap, used only for the first admin login. Remove via `fly secrets unset ADMIN_PASSWORD --app gevoelscore-backend` once you've changed it in the Directus admin UI. |

**Volumes:**

| Name | Mount | Size | Notes |
|------|-------|------|-------|
| `gevoelscore_uploads` | `/directus/uploads` (in backend container) | 1 GB | Encrypted, automatic snapshots. Empty in v1 (no file uploads yet). |

### Fly Postgres (`gevoelscore-pg`)

Self-hosted single-node Postgres on Fly, migrated from Neon on 2026-07-14 — see [ADR 0007](../decisions/0007-self-hosted-postgres-on-fly.md) for the why. Neon is fully decommissioned.

| App | Region | Database | Postgres | Nodes |
|-----|--------|----------|----------|-------|
| `gevoelscore-pg` (postgres-flex image) | `ams` | `gevoelscore` | 18 | 1 (machine `830999a71e2ee8`) |

**Volume:** `vol_r68zlzm1qxkqpqp4` — 2 GB, encrypted, automatic daily snapshots with 14-day retention. Holds the day-0 pre-migration dump at `/data/neon.dump`.

**Connection:** `gevoelscore-pg.flycast:5432` — org-internal only, no public address. Local access goes through `fly proxy 15432:5432 -a gevoelscore-pg`.

**Role:** `postgres` (superuser) — used by Directus via the `DB_CONNECTION_STRING` secret.

---

## Directus state

### Collections (9 user collections)

| Collection | Purpose | Status | v1 use |
|-----------|---------|--------|--------|
| `day_entries` | The cardinal entity — one row per local-date logged | ✅ **1,363 rows** (full historical sheet, 3-9-2022 → 27-5-2026) | **YES** — daily entries |
| `tags` | Personal/dynamic tag set (6 clusters + interventie/project/custom). Supports `parent_id` self-FK for intra-cluster hierarchy. | ✅ **83 tags seeded**, all `parent_id = null`; usage_count recomputed | **YES** — tag chips |
| `day_entries_tags` (junction) | M2M between day_entries × tags, cascading deletes, with provenance (`source`, `confidence`, `confirmed_at`) | ✅ **1,338 junction rows**, all `source='note_pattern', confidence=1.0` (auto-inferred from note regex) | **YES** — via the `tags` alias field |
| `projects` | Active interventions/projects (Citalopram, Breinvoeding, etc.) | ✅ **5 projects seeded** (Citalopram, CPAP, Naproxen, Breinvoeding, HeartMath) | Schema queryable; ProjectEntry M2M live |
| `project_field_configs` | Per-project field definitions | ✅ created | No — v1.5 |
| `project_entries` | Per-project per-day entries | ✅ created (no rows) | No — v1.5 |
| `project_entries_tags` (junction) | M2M between project_entries × tags, cascading deletes, with same provenance columns as `day_entries_tags` | ✅ created (no rows) | No — v1.5 |
| `calendar_events` | Google Calendar read-only sync | ✅ created | No — v1.5 |
| `garmin_daily` | Garmin aggregate per day | ✅ placeholder | No — v2 (separate native iOS app) |
| `health_daily` | Apple Health aggregate per day | ✅ placeholder | No — v2 |
| `weather_daily` | Weather per location per day | ✅ placeholder | No — v2 |

**Schema verification**: all 29 critical PostgreSQL type checks pass — see [`directus/scripts/verify-schema.mjs`](../../directus/scripts/verify-schema.mjs). No silent VARCHAR-where-INTEGER bugs.

**M2M shape (no longer deferred)**: both `day_entries × tags` and `project_entries × tags` are proper Directus M2M junctions with cascading deletes on both FKs and provenance columns (`source`, `confidence`, `confirmed_at`). The pre-M2M JSON-array fields (`day_entries.tag_ids`, `day_entries.project_entry_ids`, `day_entries.calendar_event_ids`, `project_entries.tag_ids`) have been removed. Cross-collection joins now happen by `date` — see [`directus/scripts/views/`](../../directus/scripts/views/) for the canonical query views (`daily_observations`, `day_tags_flat`, `tag_correlations`).

### Auth

| Type | Name | Purpose |
|------|------|---------|
| User | `<admin>` | Admin recovery user. 2FA enabled. Email + UUID stored in 1Password under "gevoelscore — Directus admin". |
| Role | `gevoelscore-frontend-api` | What the Next.js frontend's Directus user is assigned. |
| Policy | `gevoelscore-frontend-policy` | Linked to the role above. Holds the 24 permission entries (6 collections × CRUD). |

> Directus internal UUIDs are deliberately omitted from this public document. Look them up via the admin UI (Settings → Access Control) or `directus_users` / `directus_roles` / `directus_policies` table when needed.

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
├── .env.example         — Env var template (DIRECTUS_TOKEN, DIRECTUS_URL)
└── scripts/
    ├── lib/
    │   ├── directus-request.mjs       — Shared auth + fetch helper
    │   └── tag-patterns.mjs           — Canonical regex → tag mapping for semantic enrichment
    ├── setup-schema.mjs               — Creates all collections + M2Ms (idempotent, one-POST rule)
    ├── verify-schema.mjs              — Confirms PostgreSQL types match expectations
    ├── setup-permissions.mjs          — Role + policy + permissions (idempotent)
    ├── seed-tags.mjs                  — Inserts the 83 tags from tag-patterns.mjs
    ├── seed-projects.mjs              — Inserts the 5 v1 Project entities
    ├── analyze-notes.mjs              — Read-only frequency/pattern analysis of historical CSV
    ├── import-real-history.mjs        — Imports private/real-history.csv (PII), source='note_pattern'
    ├── import-sample-data.mjs         — Imports docs/sample-data.csv (60-row anonymised set)
    ├── recompute-tag-usage.mjs        — Refreshes Tag.usage_count from junction rows
    ├── upgrade-m2m-tags.mjs           — Historical: JSON tag_ids → M2M (already applied)
    ├── add-tag-provenance.mjs         — Historical: adds source/confidence/confirmed_at to junction
    ├── flatten-day-entry-json-arrays.mjs — Historical: drops JSON-array FKs + adds project_entries × tags M2M
    ├── add-tag-hierarchy.mjs          — Historical: adds tags.parent_id self-FK
    └── views/
        ├── 01-daily-observations.sql  — Wide cross-source join by date (LEFT JOINs)
        ├── 02-day-tags-flat.sql       — Denormalised day × tag rows with provenance
        └── 03-tag-correlations.sql    — Per-tag avg_score, stddev, date range, confirmed counts
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
| `src/lib/auth/rate-limit.ts` | 6 | ✅ shipped — login step 2 |
| `src/lib/auth/session.ts` | 12 | ✅ shipped — login step 2 |
| `src/lib/auth/origin-check.ts` | 9 | ✅ shipped — login step 3 |
| `src/lib/auth/directus-auth.ts` | 12 | ✅ shipped — login step 3, SDK-wrapped |
| `src/lib/auth/pending-otp.ts` | 9 | ✅ shipped — login step 4 |
| `src/lib/auth/stores.ts` | — (composed in route tests) | ✅ shipped — login step 4 |
| `src/app/page.tsx` + `layout.tsx` | (Playwright e2e) | ✅ minimal shell — login step 1 |
| `src/app/api/health/route.ts` | (Playwright API) | ✅ shipped — bootstrap smoke |
| `src/app/api/auth/login/route.ts` | 10 + Playwright | ✅ shipped — login step 4 |
| `src/app/api/auth/login/verify/route.ts` | 7 + Playwright | ✅ shipped — login step 4 |
| `src/app/api/auth/logout/route.ts` | 4 + Playwright | ✅ shipped — login step 4 |
| `src/lib/domain/streak.ts` | 7 | ✅ shipped — daily-entry step 6 |
| `src/lib/api/day-entries.ts` (SDK wrapper) | 11 | ✅ shipped — daily-entry steps 1+3 |
| `src/lib/api/tags.ts` (SDK wrapper) | 2 | ✅ shipped — daily-entry step 5 |
| `src/hooks/use-day-entry-upsert.ts` | 11 | ✅ shipped — daily-entry step 4 |
| `src/app/api/day-entries/today/route.ts` | Playwright API | ✅ shipped — daily-entry step 1 |
| `src/app/api/day-entries/route.ts` (range) | Playwright API | ✅ shipped — daily-entry step 1 |
| `src/app/api/day-entries/[date]/route.ts` (PUT upsert) | Playwright API | ✅ shipped — daily-entry step 3 |
| `src/components/score-row.tsx` (was score-wheel) | 13 | ✅ shipped — daily-entry steps 4 + 4b |
| `src/components/save-status.tsx` | 7 | ✅ shipped — daily-entry steps 4 + 4b |
| `src/components/note-field.tsx` | 5 | ✅ shipped — daily-entry step 5 |
| `src/components/tag-category-list.tsx` | 9 | ✅ shipped — daily-entry step 5 |
| `src/components/day-entry-editor.tsx` | 3 | ✅ shipped — daily-entry step 5 |
| `src/components/today-shell.tsx` | 5 | ✅ shipped — daily-entry steps 2 + 4b + 6 |
| `src/components/score-chart.tsx` | 4 | ✅ shipped — daily-entry step 6 |
| `src/components/timeline-view.tsx` | 4 | ✅ shipped — daily-entry step 6 |
| `src/components/day-detail-sheet.tsx` | (covered by timeline-view tests) | ✅ shipped — daily-entry step 6 |

**Test suite** (as of 2026-05-28, after the partial-PUT fix):
- **Vitest**: 500/500 passing (domain + auth library + route handlers + daily-entry components/hooks/SDK; +5 for the partial-update SDK + route coverage added after the deploy-time bug)
- **Playwright (chromium)**: 44/45 passing (the 1 failure is in the parallel `/over` public-landing-page work, out of daily-entry scope)
- **Live-stack Playwright**: unchanged from login step 8 — not yet extended for daily-entry routes
- **TypeScript**: `tsc --noEmit` clean
- **ESLint**: clean (flat config + jsx-a11y + security + no-secrets)
- **`npm audit`**: 2 moderate findings in `postcss` bundled inside Next.js (not actionable — awaits upstream Next patch)

---

## What's NOT yet done

In the order they should be tackled:

1. **Real-usage soak** (in progress since 2026-05-28). User installed the PWA on iOS via Add-to-Home-Screen and is logging real entries. No fixes scheduled until friction is reported. See `private/MEMORY.md` → "Soak-test mode" memory.
2. **Manual walkthroughs** (cardinal-principle gates — deferred during soak):
   - Phone stopwatch: open → tap a 7 → close ≤ 5s on a good-day simulation
   - Brainfog simulation: 2-second hesitation between intention and action — flow must tolerate
   - One-handed thumb reach across the horizontal score row
   - Keyboard-only flow through row → note → tag headers → expand → chip toggle
   - VoiceOver / TalkBack announces score changes, tag toggles, save status correctly
3. **Apply the Postgres views** (one-time, deferred until a consumer exists)
   - Run `fly proxy 15432:5432 -a gevoelscore-pg`, then apply each `directus/scripts/views/*.sql` file with `psql $env:DATABASE_URL -f <file>` (or a `pg`-based script over the same proxy).
   - Optional: register them as read-only collections in the Directus admin UI so they show up in the data studio.
4. **Track A3 compliance** ([docs/plans/2026-05-27-audit-remediation-and-standards-enforcement.md](../plans/2026-05-27-audit-remediation-and-standards-enforcement.md))
   - `directus_auth_events` collection for NEN 7510 §12.4 audit trail (route handlers carry `TODO(I3)` markers at the insertion points)
   - GDPR Art 9 special-category data declaration (health data)
   - Postgres at-rest encryption verification record (the `gevoelscore-pg` volume is encrypted)
5. **Track B4** — wire `npm run verify` to GitHub Actions CI (needs `git push origin main` first; currently no `.github/workflows/`)
6. **Wire the CSV import UI to Directus** (parser shipped; admin UI form is the gap)
7. **CSV / JSON export endpoint** + delete-all (cardinal "user-owned data" requirement; separate feature)
8. **Recent-missed-days, calendar grid, settings** screens (per [REQUIREMENTS.md](../REQUIREMENTS.md#v1-screens))

---

## First-deploy notes (2026-05-27)

Two issues caught by the first `fly deploy` of the frontend, both fixed in commit history:

1. **Tailwind v4 needs optional native deps.** The Dockerfile's deps stage originally ran `npm ci --omit=optional`. Tailwind v4 uses `lightningcss`, which ships its native binary as an optionalDependency per platform (`lightningcss-linux-x64-musl` for our Alpine target). Omitting optionals made the build fail with `Cannot find module '../lightningcss.linux-x64-musl.node'`. Fix: drop `--omit=optional`. The Dockerfile comment now flags this.
2. **Fly auto-creates 2 machines for HA.** With `min_machines_running = 1` Fly creates a SECOND machine alongside for zero-downtime deploys. Our session and rate-limit stores are in-memory per machine, so a session created on machine A would be invisible to machine B. Fix: `fly scale count 1 --app gevoelscore-frontend` after first deploy. Trade-off: brief downtime during future deploys (~30s while the new machine starts); acceptable for a single-user app where the operator IS the user.
3. **`getClientIp` trusts `Fly-Client-IP`** (audit H4 fix). Rate-limit bucket-keying reads `Fly-Client-IP` first, then `X-Real-IP`, then the *last* hop of `X-Forwarded-For`. Fly's edge sets `Fly-Client-IP` directly and the client cannot forge it. If moving off Fly, audit the precedence — accepting the first XFF hop would re-introduce the per-request bucket-rotation bypass.

If/when scaling beyond 1 machine is needed, the in-memory stores must move to a shared backend (Redis, or a `sessions` collection in Directus). The API surface in `src/lib/auth/{session,rate-limit,pending-otp}.ts` is designed for that swap — same exports, different implementation.

## Maintenance reminders

- **Directus version**: 11.17.2 (one behind 11.17.4). Bump on security advisories. Test on staging first when you set up a staging branch.
- **Fly bills**: check ~$5–7/mo. If it spikes, run `fly machine list --app gevoelscore-backend` and `fly volumes list` to see what's running.
- **Backup verification**: Fly takes daily snapshots of the `gevoelscore-pg` volume automatically (14-day retention). Once a quarter, check `fly volumes snapshots list vol_r68zlzm1qxkqpqp4` and test a restore.
