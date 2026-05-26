# gevoelscore-app

A personal Long COVID tracking app: one tap to log a daily "feeling score" (gevoelscore), optional note and tags, and a timeline view to spot patterns over time.

**Status**: pre-prototype. Requirements and technical direction are written; no code yet.

## Architecture at a glance

```
Browser PWA (Next.js)
  ↕ HTTPS, Directus SDK
Directus on Fly.io  (admin UI, auth, REST/GraphQL)
  ↕
PostgreSQL on Fly.io
```

Online-first: daily entry requires network. Offline support is a feature we'll add if real usage demands it, not a v1 requirement. The author's data analysis pipeline can query the Postgres directly.

## Why this exists

Since 3 September 2022 the author has logged a daily subjective score in a Google Sheet — 1.363 consecutive days with 100% coverage. That data has been valuable for understanding recovery patterns, interventions and energy management. The sheet is now too constrained for daily use (filtering, tagging, mobile entry are all awkward). This app aims to do exactly what the sheet does, but better on a phone.

## Cardinal principle

Daily entry must not be more friction than the current sheet. The minimum flow is **one tap for the score, done**. Anything else is optional and must not block or clutter the main screen.

## Scope

**v1** — match the current sheet on mobile:

- Daily score (1–6, half-values allowed)
- Free-text note + chip-tags
- Timeline view (30 / 90 days)
- Streak counter
- Import existing Google Sheet history
- CSV export
- Calendar view for backfill
- Works offline, mobile-first, low-stimulation UI

**v1.5** — projects/interventions, Google Calendar read-only sync.

**v2** — Apple Health (sleep, HR, HRV), Garmin via HealthKit, weather data, optional end-of-day reminder.

**Explicit non-goals (any version):** social features, AI chat, symptom encyclopedia, analytics/tracking/ads, writing to external calendars.

## Documentation

- [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) — distilled v1 user + technical requirements (start here)
- [docs/app_brief_gevoelscore.md](docs/app_brief_gevoelscore.md) — full original brief (UX, data model, roadmap)
- [docs/technisch_document.md](docs/technisch_document.md) — passive context data, integrations, privacy, licensing
- [docs/sample-data.csv](docs/sample-data.csv) — anonymized sample (60 days, date + score only)

## Tech stack

- **Frontend**: Next.js 15 (App Router, TypeScript strict) as a PWA → see [docs/decisions/0002-pwa-with-directus-backend.md](docs/decisions/0002-pwa-with-directus-backend.md)
- **Backend**: Directus (new instance, separate from any existing platform) on Fly.io
- **Database**: PostgreSQL managed by Directus on Fly.io
- **Auth**: Directus auth (token-based, single user for v1)
- **API access**: Directus SDK (`@directus/sdk`) with Zod validation at the boundary
- **Calendar (v1.5)**: Google Calendar API, read-only OAuth
- **Apple Health, Garmin (v2)**: not supported in PWA; would require a separate native iOS app that queries the same Directus backend

The original Expo decision is preserved in [docs/decisions/0001-framework-expo.md](docs/decisions/0001-framework-expo.md) (superseded). See [docs/technisch_document.md](docs/technisch_document.md) for the broader reasoning context and alternatives considered.

## Privacy

Data lives on infrastructure the author controls (self-hosted Directus + PostgreSQL on Fly.io, EU region, TLS in transit). No analytics, no tracking, no ads, no third-party telemetry, no data sold or shared. Full export and full delete are first-class features. The original "local-first" framing changed when the architecture pivoted to cloud-backed — see [ADR 0002](docs/decisions/0002-pwa-with-directus-backend.md) for the reasoning and the privacy framing in detail.

## License

- **Code**: [MIT](LICENSE)
- **Documentation**: [CC BY-SA 4.0](LICENSE-DOCS)
- **Personal data**: not licensed, not in this repo. A small anonymized sample is in `docs/sample-data.csv` for development purposes.

## Contributing

This is primarily a personal project, but issues, suggestions and PRs are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).
