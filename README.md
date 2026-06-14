# gevoelscore-app

A personal Long COVID tracking app: one tap to log a daily "feeling score" (gevoelscore), optional note and tags, and a timeline view to spot patterns over time.

**Status** (2026-05-28): domain layer + Directus backend + Next.js frontend with login + daily-entry feature (score row, note, tag picker, 30/90-day timeline with editable bottom sheet) all built, 495 vitest + 44 chromium e2e green. Login + Directus backend already deployed to Fly; the daily-entry build sits on `main` awaiting the next frontend push. See [docs/architecture/current-state.md](docs/architecture/current-state.md) for the full snapshot.

## Architecture at a glance

```
Browser PWA (Next.js 15, App Router, Tailwind v4) ← deployed: gevoelscore-frontend.fly.dev
  ↕ HTTPS, httpOnly cookie auth (gs_session)
Directus 11.17.2 on Fly.io                        ← deployed: gevoelscore-backend.fly.dev
  ↕ TLS via Neon pooler
Neon PostgreSQL 17 (EU region)                    ← deployed: gevoelscore-db
```

Online-first: daily entry requires network. Offline support is a feature we'll add if real usage demands it, not a v1 requirement.

## Why this exists

Since 3 September 2022 the author has logged a daily subjective score in a Google Sheet — 1.363 consecutive days with 100% coverage. That data has been valuable for understanding recovery patterns, interventions and energy management. The sheet is now too constrained for daily use (filtering, tagging, mobile entry are all awkward). This app aims to do exactly what the sheet does, but better on a phone.

## Cardinal principle

Daily entry must not be more friction than the current sheet. The minimum flow is **one tap for the score, done**. Anything else is optional and must not block or clutter the main screen.

## Scope

**v1** — match the current sheet on mobile:

- Daily score (integer 1–10, no halves)
- Free-text note + chip-tags across 5 clusters (mentaal / fysiek / overall / activiteit / gebeurtenis)
- Timeline view (30 / 90 days)
- Streak counter, calendar backfill view
- Import existing 1.363-day Google Sheet history
- CSV export
- Mobile-first PWA (installable via "Add to Home Screen")
- Login + 2FA (TOTP)

**v1.5** — projects/interventions tracking, Google Calendar read-only sync, richer dashboard.

**v2** — Apple Health (sleep, HR, HRV), Garmin via HealthKit, weather data, optional end-of-day reminder. These require a separate native iOS app (out of scope for the PWA) that talks to the same Directus backend.

**Explicit non-goals (any version):** social features, AI chat, symptom encyclopedia, analytics/tracking/ads, writing to external calendars.

## Repository tour

| Path | What lives here |
|------|-----------------|
| [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) | Distilled v1 user + technical requirements (start here) |
| [docs/architecture/](docs/architecture/) | System overview, current deployed state, data model, schema-management approach |
| [docs/decisions/](docs/decisions/) | Architectural Decision Records (Expo→PWA pivot, Fly+Neon infra, etc.) |
| [docs/operations/](docs/operations/) | Credentials inventory, scripts catalog, deploy/rotate/wipe runbooks |
| [docs/features/](docs/features/) | Per-feature plans + step files (TDD-shaped) |
| [docs/app_brief_gevoelscore.md](docs/app_brief_gevoelscore.md) | Full original brief (UX, data model, roadmap) — historical |
| [docs/technisch_document.md](docs/technisch_document.md) | Passive context data, integrations, privacy framing — historical |
| [docs/sample-data.csv](docs/sample-data.csv) | Anonymized sample (60 days, date + score only) |
| [src/lib/domain/](src/lib/domain/) | Pure-TS domain validators (Score, DayEntry, Tag — 232 tests) |
| [src/lib/import/](src/lib/import/) | CSV import parser (22 tests) — parses the historical sheet |
| [src/lib/auth/](src/lib/auth/) | Server-side auth primitives (rate-limit, session, pending-OTP, origin check, Directus SDK wrapper) |
| [src/app/](src/app/) | Next.js 15 App Router: minimal shell + `/api/auth/{login,login/verify,logout}` route handlers + `/api/health` |
| [tests/](tests/) | Playwright API + e2e specs (`tests/api/`, `tests/e2e/`) |
| [directus/](directus/) | Dockerfile, fly.toml, and idempotent schema/permissions scripts |
| [.claude/](.claude/) | Project-local Claude Code config: conventions, testing doctrine, security checklist, slash commands |
| [docs/research/](docs/research/) | Long COVID PEM self-research corpus: pipeline, methodology MDs, hypothesis tests, peer-review reports |

## Research-discipline methodology

The `docs/research/` track sits alongside the app and produces
analyses on a 1.363+ day personal corpus (gevoelscore + per-day
intensity + Garmin biometrics + notes + medical records). Because
the corpus is observational, single-subject, and time-series with
strong temporal dependence, no established reporting checklist
(SCRIBE 2016, CENT 2015, STROBE 2007, WWC 2022 SCED) cleanly
covers the shape of the work.

The project's own research-discipline guardrails:

- [docs/research/CONVENTIONS.md](docs/research/CONVENTIONS.md) —
  role split (producer vs reviewer), discipline gates, pre-flight
  audit hooks, project-wide anchors.
- [docs/research/reviews/](docs/research/reviews/) — a 4-layer
  peer-review checklist that adapts what transfers from each
  established standard (and explicitly states what does not) plus
  project-specific audit hooks. Verdicts must be reasoned, not
  labels.
- [docs/research/literature/methodology/](docs/research/literature/methodology/)
  — local PDFs of the standards we inherit from (CENT, STROBE,
  Daza 2018 on self-tracked n-of-1 counterfactual analysis, WWC
  2022 SCED handbook, Natesan Batley 2023 systematic review).

The act of building these review standards — adapted for
observational n=1 time-series rather than copy-pasted from
intervention-focused SCED checklists — is itself part of the
project's methodology. The 2023 systematic review found that only
3.48% of published n-of-1 medical studies meet WWC SCED evidence
standards; documenting our own adaptations is how we avoid
joining the 96.52%.

## Tech stack

- **Frontend**: Next.js 15 (App Router, TypeScript strict) + Tailwind CSS v4 as a PWA — see [ADR 0002](docs/decisions/0002-pwa-with-directus-backend.md)
- **Backend**: Directus 11.17.2 on Fly.io (`ams` region)
- **Database**: Neon PostgreSQL 17 (`aws-eu-central-1`, free tier) — see [ADR 0003 amendment](docs/decisions/0003-directus-fly-infra-setup.md#amendment-2026-05-27-postgres-provider-switched-to-neon) for the Fly-Postgres → Neon pivot
- **Auth**: Directus auth (email + password + mandatory TOTP 2FA); server-side session map + `httpOnly` cookie via Route Handlers
- **API access (frontend)**: `@directus/sdk` v18 — typed query builder, M2M-aware
- **API access (server scripts)**: plain `fetch` — dep-free, see [directus/scripts/lib/directus-request.mjs](directus/scripts/lib/directus-request.mjs)
- **Domain layer**: pure TypeScript, runs in Node + browser, zero third-party deps
- **Testing**: Vitest for unit + Playwright for API + e2e (TDD-mandatory — see [`.claude/testing.md`](.claude/testing.md))
- **Calendar (v1.5)**: Google Calendar API, read-only OAuth
- **Apple Health, Garmin (v2)**: not supported in PWA — would require a separate native iOS app

The original Expo decision is preserved in [ADR 0001](docs/decisions/0001-framework-expo.md) (superseded).

## Privacy

Data lives on infrastructure the author controls — self-hosted Directus + Neon-managed Postgres in an EU region, behind TLS, behind 2FA. No analytics, no tracking, no ads, no third-party telemetry, no data sold or shared. Full export (CSV / JSON / Postgres dump) and full delete are first-class.

The original "local-first" framing changed when the architecture pivoted to cloud-backed — see [ADR 0002](docs/decisions/0002-pwa-with-directus-backend.md) for the reasoning and the privacy framing in detail.

## License

- **Code**: [MIT](LICENSE)
- **Documentation**: [CC BY-SA 4.0](LICENSE-DOCS)
- **Personal data**: not licensed, not in this repo. A small anonymized sample is in `docs/sample-data.csv` for development purposes.

## Contributing

This is primarily a personal project, but issues, suggestions and PRs are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

For development workflow conventions, the TDD doctrine, the OWASP-ASVS-aligned security checklist, and the slash commands available to Claude Code in this repo, see [`.claude/`](.claude/).
