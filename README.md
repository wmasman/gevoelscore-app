# gevoelscore-app

A personal Long COVID tracking app: one tap to log a daily "feeling score" (gevoelscore), optional note and tags, and a timeline view to spot patterns over time.

**Status**: pre-prototype. Requirements and technical direction are written; no code yet.

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

- **Framework**: Expo (React Native), managed workflow → see [docs/decisions/0001-framework-expo.md](docs/decisions/0001-framework-expo.md)
- **Local storage**: SQLite via `expo-sqlite`; encryption via community package (e.g. `op-sqlite` with SQLCipher)
- **Build / distribution**: EAS Build (cloud iOS compilation, no Mac needed) + EAS Submit
- **Cloud sync**: opt-in, aggregates only, deferred to v2 (Supabase candidate)
- **Calendar (v1.5)**: Google Calendar API, read-only OAuth
- **Apple Health (v2)**: `react-native-health` bridge + targeted Swift native modules where the bridge falls short

See [docs/technisch_document.md](docs/technisch_document.md) for the broader reasoning and alternatives considered.

## Privacy

Local-first. Raw health data and personal notes never leave the device without explicit, per-source opt-in. No analytics, no tracking, no ads. Full export and full delete are first-class features.

## License

- **Code**: [MIT](LICENSE)
- **Documentation**: [CC BY-SA 4.0](LICENSE-DOCS)
- **Personal data**: not licensed, not in this repo. A small anonymized sample is in `docs/sample-data.csv` for development purposes.

## Contributing

This is primarily a personal project, but issues, suggestions and PRs are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).
