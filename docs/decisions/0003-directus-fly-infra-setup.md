# ADR 0003: Directus + Fly.io infrastructure setup

- **Status**: Accepted
- **Date**: 2026-05-26 (amended 2026-05-27: Postgres provider switched from Fly Postgres to Neon — see "Amendment 2026-05-27" below)
- **Builds on**: [ADR 0002](0002-pwa-with-directus-backend.md) (which chose the stack; this ADR commits to the specific provisioning shape)
- **Deciders**: Willem Masman (author), Claude (AI collaborator)

## Amendment 2026-05-27: Postgres provider switched to Neon

During provisioning, the Postgres choice was changed from **Fly Managed Postgres** to **Neon Postgres** (matching the TVO platform pattern, which also runs Directus-on-Fly + Neon).

**Why the switch:**
- TVO already uses Neon for the same Directus-on-Fly shape (`programmeerprobeer/directus/docs/staging-setup.md`). Aligning gevoelscore on the same DBaaS reduces mental overhead and means one tool (`neonctl`) for both.
- Neon free tier supports our load (single user, ~1,400 historical rows + ~365 new rows/year) indefinitely.
- Branching: trivial to spin off a staging branch later if needed, instant copy of prod data — useful for testing destructive migrations.
- Scales to zero when idle (~1s cold start on first request after idle). Acceptable for a personal app where the user-facing slow path is "you opened the app for the first time today" — adds ≤1s to a cardinal sub-10s budget, only on cold-start.

**What changed concretely:**
- Provisioned **Neon project `gevoelscore-db`** under the existing `tvo-backend-database` org (same billing entity, separate Neon project — full isolation from TVO data per the [[project-infra-plan]] memory).
- Region: `aws-eu-central-1` (Frankfurt — Neon's nearest EU region; `ams` not available in Neon).
- Postgres version: 17 (Neon default).
- The Fly Postgres `gevoelscore-db` that was briefly created in the same session was **destroyed** before any data was written.
- Fly secrets `DB_CLIENT=pg` + `DB_CONNECTION_STRING=postgresql://...neon.tech/neondb?sslmode=require` (pooler endpoint) were set on `gevoelscore-backend` instead of `fly postgres attach`.

**What stays the same:**
- Everything else from this ADR — Fly app names, regions for the apps themselves, resource sizes, CORS rules, no telemetry.
- The Directus instance still runs on Fly.io, just talks to Neon instead of a Fly-managed Postgres.

## Context

ADR 0002 locked the stack as Next.js 15 PWA + Directus on Fly.io + PostgreSQL. It deliberately did not commit to specific Fly.io app names, regions, environment splits, resource sizes, or naming conventions — those were "to be decided at infra-setup time."

That time is now. This ADR commits to those choices so the schema runbook, the login feature, and any future deploy script have a single concrete target to deploy against.

The pattern is borrowed from the TVO platform's Fly.io setup (`programmeerprobeer/directus/fly.toml`, `programmeerprobeer/tvoo_frontend/fly.toml`), adapted for a single-user personal app with stricter privacy and no telemetry.

## Options reconsidered

### Single environment vs. staging + production

- **Single environment** (one Fly.io app pair): simplest. Direct deploys. Half the cost. Risk: a bad deploy breaks daily logging. Mitigation: feature branches + automated tests as a quality gate (we already have 233 tests passing).
- **Staging + production**: matches TVO pattern. Test changes against staging before promoting. ~2x cost. Overkill for a single-user app where the user is also the developer (you'll know within a minute if a deploy broke).

**Chosen**: **Single environment** for v1. Add staging if the deploy pace + risk profile changes.

### Region

- **Amsterdam (`ams`)**: matches TVO pattern. Closest to author's location. EU jurisdiction for personal health data (GDPR-relevant). Same data-residency story as the original local-first framing in spirit.
- Other EU regions: no specific advantage; `ams` is well-served by Fly.io.

**Chosen**: **`ams`** — primary region for both apps and Postgres.

### Naming

- TVO uses `tvo-backend-staging` / `tvo-frontend-staging` patterns. For gevoelscore: same shape but with the `gevoelscore-` prefix.
- App names on Fly.io are globally unique; if either taken, fall back to `gvscore-backend` / `gvscore-frontend`.

**Chosen**: **`gevoelscore-backend`** and **`gevoelscore-frontend`** (with fallback prefixes ready).

### Resource sizes

- Backend (Directus): 1 GB RAM, 1 shared CPU (matches TVO pattern; Directus needs the RAM for upload processing).
- Frontend (Next.js): 512 MB RAM, 1 shared CPU (matches TVO frontend; SSR is light for a single user).
- Postgres: smallest tier with backups enabled. Fly.io's default `shared-cpu-1x` 256 MB Postgres is enough for thousands of daily entries.

**Chosen**: matches TVO sizes for backend/frontend; smallest Postgres tier.

### TVO's PostHog analytics — NOT carried over

TVO's frontend fly.toml has `NEXT_PUBLIC_POSTHOG_KEY` configured. The gevoelscore cardinal principle is **no telemetry, no tracking, no analytics**. PostHog is explicitly excluded.

**Chosen**: **no PostHog**, no analytics SDK of any kind. The TVO pattern is followed structurally but stripped of telemetry hooks.

## Decision

### Backend app: `gevoelscore-backend`

```toml
# fly.toml — backend
app = 'gevoelscore-backend'
primary_region = 'ams'

[[mounts]]
  source = 'gevoelscore_uploads'   # for any future file uploads; empty in v1
  destination = '/directus/uploads'

[http_service]
  internal_port = 8055
  force_https = true
  auto_stop_machines = 'off'
  auto_start_machines = true
  min_machines_running = 1

[[vm]]
  memory = '1gb'
  cpu_kind = 'shared'
  cpus = 1

[env]
  HOST = "::"
  PORT = "8055"
  TZ = "Europe/Amsterdam"
  # KEY = "..."   set via `fly secrets set` — never committed
  # ADMIN_EMAIL / ADMIN_PASSWORD — set via `fly secrets set` for bootstrap, change immediately
  # DB_CONNECTION_STRING — provided automatically when attaching Fly Postgres
  # PUBLIC_URL = "https://gevoelscore-backend.fly.dev"
  # CORS_ENABLED = "true"
  # CORS_ORIGIN = "https://gevoelscore-frontend.fly.dev"   strict allowlist per security-checklist
  # CORS_CREDENTIALS = "true"   needed for httpOnly cookie auth
```

### Frontend app: `gevoelscore-frontend`

```toml
# fly.toml — frontend
app = "gevoelscore-frontend"
primary_region = "ams"

[build]
  dockerfile = "Dockerfile"
  [build.args]
    NEXT_PUBLIC_DIRECTUS_URL = "https://gevoelscore-backend.fly.dev"
    NEXT_PUBLIC_APP_URL = "https://gevoelscore-frontend.fly.dev"
    # NO PostHog — telemetry is forbidden per the cardinal principles

[env]
  NODE_ENV = "production"
  NEXT_TELEMETRY_DISABLED = "1"
  PORT = "3000"
  HOSTNAME = "0.0.0.0"
  NEXT_PUBLIC_DIRECTUS_URL = "https://gevoelscore-backend.fly.dev"
  DIRECTUS_URL = "http://gevoelscore-backend.internal:8055"   # server-side, internal Fly network
  NEXT_PUBLIC_APP_URL = "https://gevoelscore-frontend.fly.dev"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1
  [[http_service.checks]]
    grace_period = "10s"
    interval = "30s"
    method = "GET"
    timeout = "5s"
    path = "/api/health"

[[vm]]
  size = "shared-cpu-1x"
  memory = "512mb"

[deploy]
  strategy = "rolling"
  max_unavailable = 1

# No [metrics] section — no telemetry export.
```

### Postgres

- Fly.io Postgres, attached to `gevoelscore-backend`
- Region `ams`
- Smallest available tier with automatic backups
- Connection string injected as `DATABASE_URL` or `DB_CONNECTION_STRING` env var when attached
- Backups enabled by default (Fly retains 24h + 7-day snapshots)

### Secrets (set via `fly secrets set`, never committed)

Backend:
- `KEY` — Directus encryption key (32-byte random hex)
- `SECRET` — Directus auth secret (32-byte random hex)
- `ADMIN_EMAIL` — initial admin (you), changed/disabled after bootstrap
- `ADMIN_PASSWORD` — initial admin password, changed immediately
- `DB_CLIENT` = `pg`, `DB_CONNECTION_STRING` — auto-set on Postgres attach
- `EMAIL_FROM`, `EMAIL_TRANSPORT` etc. — defer until email is actually needed

Frontend:
- (None for v1 — the public env vars in [env] are enough. Future OAuth callback secrets go here.)

## Commitments

| Layer | Commitment |
|---|---|
| Backend app name | `gevoelscore-backend` (fallback: `gvscore-backend` if taken) |
| Frontend app name | `gevoelscore-frontend` (fallback: `gvscore-frontend`) |
| Postgres | Fly.io managed, attached to backend, smallest tier |
| Region | `ams` everywhere |
| Environments | **One** (no staging/production split) |
| Resource sizes | 1 GB backend, 512 MB frontend, smallest Postgres tier |
| TLS | Force HTTPS on both apps; Fly handles certs |
| Auth | Directus default (token + 2FA TOTP per ADR 0002) |
| CORS | Allowlist only the frontend's origin (no wildcards) — set via `CORS_ORIGIN` env var |
| Telemetry | **None** — no PostHog, no Sentry, no analytics, no metrics export |
| Backups | Fly.io Postgres automatic snapshots (24h + 7d default) |

## Setup runbook

Lives in [docs/architecture/directus-setup.md](../architecture/directus-setup.md) (next deliverable). That doc contains the exact `flyctl` commands, the Directus collection schemas to create via admin UI, the CORS configuration, and the bootstrap sequence.

## Consequences

### Positive
- One concrete deploy target — schema runbook, login feature, future deploy scripts all have an unambiguous destination.
- TVO pattern reused — known-good shape, minimal cognitive overhead.
- ~$5–10/month total Fly cost (backend + frontend + small Postgres) — within personal-project budget.
- All EU-resident — clean GDPR story even though it's the user's own data.

### Negative
- Single environment means breaking changes hit production immediately. Mitigation: 233 tests + manual smoke before deploy.
- Fly.io is a single vendor dependency. Mitigation: Directus is portable (Postgres dump + admin export → import elsewhere); Next.js is portable (any Node host).
- The author becomes their own SRE for uptime. Acceptable given the daily-logging tolerance for "no network, retry" failure mode (per ADR 0002 — daily entry is allowed to fail; the UX of that failure is not).

### Migration cost if revisited
- Adding staging environment later: ~1–2 hours (clone fly.toml, duplicate Postgres, add CI env split). Data model survives because schema lives in Directus admin.
- Moving region: Postgres restore from snapshot + redeploy ~30 minutes downtime.
- Moving off Fly.io: Postgres dump + redeploy elsewhere ~1 day. Data model is portable.

## When to revisit

Revisit this ADR if:
- The single-environment risk profile changes (multiple developers, more frequent deploys, higher uptime stakes)
- Fly.io pricing or terms change
- Backend or frontend resource needs grow beyond the chosen sizes
- A second user joins (different security/scaling profile)

## What's NOT in this ADR (intentionally deferred)

- **Domain name** — `gevoelscore-backend.fly.dev` / `gevoelscore-frontend.fly.dev` are the Fly defaults. Custom domain via `fly certs` is a v1.5 nice-to-have, not a v1 requirement.
- **Email delivery** — no transactional email in v1 (no register flow, no password reset). Defer Brevo/SES until needed.
- **CI/CD** — manual `fly deploy` is fine for v1's pace. Add GitHub Actions when commit-to-deploy becomes friction.
- **Monitoring/alerting** — no telemetry deps, so monitoring is "check the app loads when you open it." Add Fly.io's built-in health-check alerts (free) only if uptime becomes a real concern.

## References

- [ADR 0002](0002-pwa-with-directus-backend.md) (the stack choice)
- [docs/architecture/directus-setup.md](../architecture/directus-setup.md) (the runbook this ADR points to)
- [.claude/security-checklist.md](../../.claude/security-checklist.md) (CORS, secrets, no-telemetry rules)
- TVO Fly.io reference pattern: `programmeerprobeer/directus/fly.toml`, `programmeerprobeer/tvoo_frontend/fly.toml`
