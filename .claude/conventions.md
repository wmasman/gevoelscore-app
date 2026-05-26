# Conventions & proposed structure

Loaded on demand by Claude when it needs file-layout or coding-convention details. Linked from [CLAUDE.md](../CLAUDE.md).

> Cardinal principles, scope, and tech-stack live in the source-of-truth docs, not here:
> - Cardinal principles + v1 requirements → [docs/REQUIREMENTS.md](../docs/REQUIREMENTS.md)
> - UX, data model, version roadmap → [docs/app_brief_gevoelscore.md](../docs/app_brief_gevoelscore.md)
> - Tech stack, integrations, privacy → [docs/technisch_document.md](../docs/technisch_document.md) + [README.md](../README.md)

---

## Proposed file structure (once code exists)

Per [ADR 0002](../docs/decisions/0002-pwa-with-directus-backend.md), the stack is Next.js 15 (App Router) + Directus backend.

```
src/
  app/                  — Next.js App Router (root layout, daily page, timeline, calendar, settings, import, export)
  components/           — shared React components (ScoreButton, TagChip, etc.)
  lib/
    api/                — Directus SDK client + typed query/mutation wrappers (the only place that knows the API surface)
    domain/             — DayEntry, Tag, Project — typed domain logic, pure TS, no platform imports
    validation/         — Zod schemas at API boundaries (CSV import, Directus response shape)
    integrations/       — per-source modules (google-calendar v1.5, weather v2) with shared "fetch + aggregate + store per day" interface
    import/             — Google Sheet / CSV / XLSX importers
    export/             — CSV / JSON exporters
  hooks/                — React hooks (data fetching, form state)
  __tests__/            — co-located by module (prefer per-module __tests__/ over a top-level test folder)
public/                 — static assets (icons, manifest.webmanifest, robots.txt)
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
