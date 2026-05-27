# System overview

What runs where, what depends on what, what data flows across which boundary.

---

## High-level diagram

```
                                   ┌─────────────────────────────────────┐
                                   │  Browser (Safari iOS primary,       │
                                   │  Chrome / Firefox cross-check)      │
                                   │                                     │
                                   │  PWA installable via Add-to-Home    │
                                   └────────────────┬────────────────────┘
                                                    │
                                                    │ HTTPS — cookie auth
                                                    │ (httpOnly, Secure, SameSite=Strict)
                                                    ▼
                                   ┌─────────────────────────────────────┐
                                   │  Next.js 15 app (App Router)        │
                                   │  Fly.io app: gevoelscore-frontend   │
                                   │  Region: ams                        │
                                   │  ⚠ NOT YET DEPLOYED — slot only     │
                                   │                                     │
                                   │  • Route Handlers proxy Directus    │
                                   │  • Server components fetch via      │
                                   │    DIRECTUS_URL (internal Fly net)  │
                                   │  • Browser code never sees tokens   │
                                   └────────────────┬────────────────────┘
                                                    │
                                                    │ HTTP (internal Fly network)
                                                    │ http://gevoelscore-backend.internal:8055
                                                    ▼
                                   ┌─────────────────────────────────────┐
                                   │  Directus 11.17.2                   │
                                   │  Fly.io app: gevoelscore-backend    │
                                   │  Region: ams                        │
                                   │  1 GB RAM, 1 shared CPU             │
                                   │                                     │
                                   │  Public URL: gevoelscore-backend    │
                                   │              .fly.dev               │
                                   │  Admin UI: /admin                   │
                                   │  REST API: /items, /auth, /users    │
                                   └────────────────┬────────────────────┘
                                                    │
                                                    │ TLS via Neon pooler
                                                    │ postgres://...@ep-flat-grass-
                                                    │ alwa40oq-pooler...neon.tech
                                                    ▼
                                   ┌─────────────────────────────────────┐
                                   │  Neon Postgres 17                   │
                                   │  Project: gevoelscore-db            │
                                   │  Region: aws-eu-central-1           │
                                   │  Free tier (scales to zero)         │
                                   │  Daily automatic backups            │
                                   └─────────────────────────────────────┘
```

---

## Data path: a daily-entry tap

User taps score `5` on the Home/Daily screen → save chain:

1. **Client side** — `validateScore(5)` from `src/lib/domain/score.ts` returns `{ ok: true, value: 5 }`. No network.
2. **Optimistic UI** — score button shows selected immediately; "saving…" indicator appears.
3. **`fetch('/api/day-entries/today', { method: 'PATCH', body: {...} })`** — same-origin, sends the `httpOnly` session cookie automatically.
4. **Next.js Route Handler** — reads session cookie, looks up Directus access token from in-memory map, validates `Origin` header against the configured frontend origin (CSRF stop per [security-checklist A08](../../.claude/security-checklist.md)).
5. **Directus SDK call** — `directus.items('day_entries').updateByQuery({ filter: { date: today } }, { score: 5 })`. Goes over the internal Fly network (`http://gevoelscore-backend.internal:8055`), no TLS overhead.
6. **Directus** — checks the user's role (`gevoelscore-frontend-api`) has `update` on `day_entries` → yes → translates to SQL `UPDATE day_entries SET score = 5, updated_at = now() WHERE date = today RETURNING *`.
7. **Neon Postgres** — applies the UPDATE. ~10–50ms typically; cold-start adds up to ~1s the first time after idle.
8. **Response bubbles back** — Directus returns the updated row → Route Handler returns it to client → client confirms via the "saved" affordance.

Total expected: well under 200ms warm, ~1.2s cold-start. Cardinal sub-10s budget has lots of room.

---

## Reading the database (the query surface)

Three layers, pick the lowest one that answers the question:

1. **Directus REST API / SDK** for entity-with-relations reads from the application (user auth applies).
2. **Postgres views** (`daily_observations`, `day_tags_flat`, `tag_correlations`) for cross-source aggregation. Read-only, bypass Directus.
3. **Raw SQL** for one-off analysis via Neon Console.

The join key across all daily-grain entities is `date` — there are no id-arrays linking `day_entries` to child collections. See [queries-and-views.md](queries-and-views.md) for the full guide and [ADR 0004](../decisions/0004-tag-provenance-date-joins-and-tag-hierarchy.md) for the rationale.

---

## Trust boundaries

| Boundary | What crosses | What's enforced |
|----------|-------------|-----------------|
| **Browser → Next.js** | Cookies (auth), JSON (mutations) | Origin/Referer check; rate-limit on login endpoints; CSP headers |
| **Next.js Route Handler → Directus** | Directus SDK calls with admin/role token | TLS-only public path; internal Fly network for server-server; token never leaks to client |
| **Directus → Neon** | SQL via pooled connection | TLS-required Postgres connection; password in Fly secret; Neon role-level permissions (`neondb_owner`) |
| **Public web → Backend admin UI** | Browser auth (admin login + TOTP) | 2FA required; admin role gated behind Directus auth |
| **Public web → Backend /items/*** | None — no anonymous access | Directus public role has zero read permissions on user collections |

---

## What's deployed vs. planned

| Component | Status | Notes |
|-----------|--------|-------|
| Directus backend | ✅ Deployed | gevoelscore-backend.fly.dev — 11.17.2, healthy |
| Neon Postgres | ✅ Live | Free tier; scales to zero when idle |
| Directus schema (9 user collections + 2 M2M junctions) | ✅ Created | All PostgreSQL types verified (29/29). M2M junctions carry provenance (source, confidence, confirmed_at) per [ADR 0004](../decisions/0004-tag-provenance-date-joins-and-tag-hierarchy.md). |
| Postgres views (`daily_observations`, `day_tags_flat`, `tag_correlations`) | ✅ Applied via Neon Console | Read-only query surface; see [queries-and-views.md](queries-and-views.md) |
| Role + policy + permissions | ✅ Configured | gevoelscore-frontend-api role, 24 permissions |
| Frontend-app Directus user | ⏳ Manual step | You create via admin UI when wiring up frontend |
| Next.js frontend code | ❌ Not started | Feature plan exists ([docs/features/login/](../features/login/)) |
| Next.js Fly app deploy | ❌ Slot only | App slot `gevoelscore-frontend` exists, no machines |
| CSV import wired to Directus | ❌ Parser ready, integration pending | [src/lib/import/csv-day-entries.ts](../../src/lib/import/csv-day-entries.ts) parses; needs upsert-to-Directus glue |
| Domain validation library | ✅ Shipped | 254/254 tests; `src/lib/domain/*` |

---

## Costs (rough)

Estimated monthly recurring:

- **Fly.io**: 1 backend machine (1 GB RAM, mostly-on) + 1 frontend machine (512 MB, eventually) ≈ $4–7/mo
- **Fly.io volume**: 1 GB encrypted ≈ $0.15/mo
- **Neon**: free tier — $0 (until you hit free-tier limits, which a single-user app effectively never will)

**Total: ~$5–7/mo**. Matches [ADR 0003](../decisions/0003-directus-fly-infra-setup.md)'s estimate.

---

## When a component fails

Quick map of "where do I go when X is broken":

| Symptom | First place to look |
|---------|--------------------|
| Daily-entry can't save | Network tab in browser → which step in the data path failed |
| Backend 502 / timing out | `fly logs --app gevoelscore-backend` — check for crash or DB connection failure |
| Backend up but writes failing | Check Neon's connection limit + status at console.neon.tech |
| Schema mismatch / "field not found" | [`docs/architecture/data-model.md`](data-model.md) vs. Directus admin UI; run `verify-schema.mjs` |
| Admin UI 403s for the frontend user | [`docs/architecture/directus-schema-management.md`](directus-schema-management.md) — verify role ↔ policy ↔ permission chain |
| Costs spike | [`docs/operations/credentials.md`](../operations/credentials.md) → who has access to provision more resources |

For full operational procedures, see [`docs/operations/runbooks/`](../operations/runbooks/).
