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
  app/                  — Next.js App Router (root layout, daily page, timeline, settings, future: import, export)
  components/           — shared React components (ScoreButton, TagChip, etc.); /lab subfolder for in-flight composites
  lib/
    api/                — Directus SDK client + typed query/mutation wrappers (the only place that knows the API surface). Result<T, E> helper lives here.
    auth/               — session store, validators, rate-limiters, origin-check (the gates every Route Handler shares)
    domain/             — DayEntry, Tag, Episode, Score, etc. — typed domain logic + validators, pure TS, no platform imports. THIS is where boundary validation lives — there is no separate `validation/` folder (see "Boundary validation via domain validators" above).
    import/             — CSV importer for the historical Google Sheet (`csv-day-entries.ts`); add v1.5+ XLSX / other-format importers here.
    ui/                 — small UI utilities (cn, focus-trap, scroll-lock, etc.)
    (future) integrations/ — per-source modules (google-calendar v1.5, weather v2, garmin v2). Add when the first integration lands; not scaffolded preemptively.
    (future) export/    — CSV / JSON exporter. Add when v1.5+ export ships; not scaffolded preemptively.
  hooks/                — React hooks (data fetching, form state, auto-save)
public/                 — static assets (icons, manifest.webmanifest, robots.txt)
docs/
  features/{name}/      — per-feature plans (README + step-N-*.md), created via /plan-feature
  decisions/            — ADRs
directus/scripts/       — idempotent Directus REST migration + setup scripts (one POST per collection / field; never `schema apply`)
scripts/                — local-developer tooling (PowerShell wrappers for env-loading, smoke tests, codegen helpers)
```

Reflects the actual layout as of 2026-06-02. `validation/` was originally proposed for Zod schemas; the codebase settled on domain-validator pattern instead. `integrations/` and `export/` are listed as `(future)` placeholders — add the folder the first time you actually need it.

---

## Code conventions

- **TypeScript strict.** No implicit `any`, no `Record<string, any>` for domain data.
- **Boundary validation via domain validators.** External data (Directus API responses, request bodies on Next.js Route Handlers) is validated at the boundary by pure-TS validators in `src/lib/domain/*` returning the discriminated `Result<T, E>` shape `{ ok: true, value: T } | { ok: false, error: ErrorVariant }`. The validator output is the typed domain value — there is no separate "parse vs validate" step. Strict-shape checks (a `REQUIRED_KEYS` const + sorted-key comparison) reject objects with missing or extra keys so a renamed Directus column surfaces immediately rather than passing through silently. Examples: `validateEpisode`, `validateTag`, `validateDayEntry`, `validateScore`, `validateDateRange`. **Do not** introduce Zod or any other schema-validation library as a default — the imperative-validator pattern is established (60+ test files) and the per-error-variant precision is load-bearing for the route handlers' HTTP error mapping. Zod (or similar) MAY be introduced scoped to a specific wide unstructured boundary if the imperative version becomes painful — likely candidates are CSV import (roadmap), LLM JSON parsing (v2), or external integration feeds (v2). Decision belongs in the relevant feature's ADR, not a project-wide refactor.
- **Filenames**: kebab-case (`score-button.tsx`, `day-entry.ts`). Tests co-located in `__tests__/`.
- **No telemetry dependencies.** Reject packages that phone home — crash reporters, analytics SDKs, A/B tools. If a package needs this disabled via config, disable it and document why.

## Copy & language

- **User-facing copy**: Dutch.
- **Code, comments, commits, planning docs**: English.
- **Domain terms stay Dutch** where the brief / REQUIREMENTS use them: `gevoelscore`, `dagboek`, `blok 1`, `mentaal/fysiek/overall/activiteit/gebeurtenis` (the v1 tag clusters — supersedes the brief's original 4-cluster `fysiek/mentaal/positief/activiteit`; see [data-model.md](../docs/architecture/data-model.md) "Why these 5 clusters"), `rustdag/licht/matig/zwaar`.

## Repo hygiene

- **No PII.** The 1.363-day personal dataset stays out. Only the anonymized [docs/sample-data.csv](../docs/sample-data.csv) is allowed. Same for OAuth tokens, API keys, location coordinates — env vars or local config only.
- **Licenses**: code [MIT](../LICENSE), docs [CC BY-SA 4.0](../LICENSE-DOCS). Check dependency licenses; no GPL deps in MIT code.
