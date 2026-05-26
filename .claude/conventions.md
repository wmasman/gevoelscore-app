# Conventions & proposed structure

Loaded on demand by Claude when it needs file-layout or coding-convention details. Linked from [CLAUDE.md](../CLAUDE.md).

> Cardinal principles, scope, and tech-stack live in the source-of-truth docs, not here:
> - Cardinal principles + v1 requirements → [docs/REQUIREMENTS.md](../docs/REQUIREMENTS.md)
> - UX, data model, version roadmap → [docs/app_brief_gevoelscore.md](../docs/app_brief_gevoelscore.md)
> - Tech stack, integrations, privacy → [docs/technisch_document.md](../docs/technisch_document.md) + [README.md](../README.md)

---

## Proposed file structure (once code exists)

```
src/
  screens/              — top-level screen components (Daily, Timeline, Calendar, Settings, Import, Export)
  components/           — shared UI primitives (ScoreButton, TagChip, etc.)
  lib/
    db/                 — SQLite schema, migrations, query helpers
    domain/             — DayEntry, Tag, Project — typed domain logic, no UI
    integrations/       — per-source modules (healthkit, google-calendar, weather, garmin) with shared "fetch + aggregate + store per day" interface
    import/             — Google Sheet / CSV / XLSX importers
    export/             — CSV / JSON / SQLite dump exporters
  hooks/                — React hooks
  __tests__/            — co-located by module (prefer per-module __tests__/ over a top-level test folder)
app/                    — Expo Router screens (if Expo Router is chosen)
docs/
  features/{name}/      — per-feature plans (README + step-N-*.md), created via /plan-feature
```

Suggestion, not a constraint, until code exists. Revisit in the prototyping phase.

---

## Code conventions

- **TypeScript strict.** No implicit `any`, no `Record<string, any>` for domain data. External data (HealthKit, Google Calendar, weather APIs, CSV import) validated at the boundary.
- **Filenames**: kebab-case (`score-button.tsx`, `day-entry.ts`). Tests co-located in `__tests__/`.
- **No telemetry dependencies.** Reject packages that phone home — crash reporters, analytics SDKs, A/B tools. If a package needs this disabled via config, disable it and document why.

## Copy & language

- **User-facing copy**: Dutch.
- **Code, comments, commits, planning docs**: English.
- **Domain terms stay Dutch** where the brief uses them: `gevoelscore`, `dagboek`, `blok 1`, `fysiek/mentaal/positief/activiteit`, `rustdag/licht/matig/zwaar`.

## Repo hygiene

- **No PII.** The 1.363-day personal dataset stays out. Only the anonymized [docs/sample-data.csv](../docs/sample-data.csv) is allowed. Same for OAuth tokens, API keys, location coordinates — env vars or local config only.
- **Licenses**: code [MIT](../LICENSE), docs [CC BY-SA 4.0](../LICENSE-DOCS). Check dependency licenses; no GPL deps in MIT code.
