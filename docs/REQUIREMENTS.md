# Requirements — v1

Distilled from [app_brief_gevoelscore.md](app_brief_gevoelscore.md) and [technisch_document.md](technisch_document.md). This file is the short version. The two longer docs hold the reasoning and alternatives.

---

## Cardinal principles

These are hard constraints. A v1 that violates them is a failure regardless of feature count.

1. **One-tap entry**: a complete day requires one tap. Nothing else is mandatory.
2. **Sub-10-second goal**: open app, log score, optionally type a note, close. ≤ 10 seconds on a good day.
3. **No friction in the main flow**: dropdowns, sliders, required tags or multi-step forms on the daily screen are forbidden.
4. **Low cognitive load**: usable on a "4-out-of-6 day" with brainfog. No flashing colors, no unnecessary animations, no sound.
5. **No notifications, ads, analytics, or tracking** (the optional end-of-day reminder is v2 and silent).
6. **User-owned data**: data lives on infrastructure the author controls (self-hosted Directus + Postgres). No third-party telemetry, no data sold or shared. Full export and full delete are first-class features. _(Note: this principle changed from the original "local-first" framing when the architecture pivoted to cloud-backed — see [ADR 0002](decisions/0002-pwa-with-directus-backend.md).)_

---

## User requirements (v1)

### Must-have

- [ ] Log a daily score: integer 1–6 only (no halves, no decimals). Nuance lives in `note` and tags — see [architecture/data-model.md](architecture/data-model.md) (DayEntry, "Score validation") for the rationale
- [ ] Optional free-text note per day (no length limit)
- [ ] Optional chip-tags per day, multi-select
- [ ] Tag set is personal and dynamic: frequently used tags surface, rarely used tags fade
- [ ] Seed tag set in four clusters (fysiek / mentaal / positief / activiteit) — see brief for content
- [ ] User can add, rename, archive and merge tags
- [ ] Timeline view: last 30 days and last 90 days, simple line chart
- [ ] Streak counter (consecutive days logged)
- [ ] Calendar view for backfill — empty days clearly marked, one tap to fill
- [ ] Import existing 1.363-day Google Sheet (CSV/XLSX): column B → score, column C → note
- [ ] Export everything to CSV at any time
- [ ] Online-first (daily entry requires network connectivity; offline support is a v1.5+ feature, not a v1 requirement — see [ADR 0002](decisions/0002-pwa-with-directus-backend.md) for the deliberate scope shift)
- [ ] Mobile-first responsive UI (designed for one-handed phone use in bed, installable as PWA via "Add to Home Screen")

### Out of scope for v1

- Projects / interventions tracking (v1.5)
- Google Calendar sync (v1.5)
- Apple Health, Garmin, weather data (v2)
- Sub-scores, end-of-day reminder, bonus fields (v2)
- Cloud sync (opt-in, v2 at earliest)
- AI / chat / coaching features (never)
- Social / sharing / multi-user (never)

---

## Technical requirements (v1)

### Framework

**Decision: Next.js 15 PWA with Directus backend on Fly.io.** See [decisions/0002-pwa-with-directus-backend.md](decisions/0002-pwa-with-directus-backend.md) for the reasoning (supersedes [0001-framework-expo.md](decisions/0001-framework-expo.md)).

- [x] Mobile-first responsive — installable as PWA, works on any modern browser
- [x] Author's Next.js / TypeScript stack — direct match with TVO infrastructure
- [x] No Apple platform friction — no Apple Developer Program, no App Store review, instant updates
- [x] Cloud is source of truth — multi-device, schema admin UI, file uploads all free via Directus
- [x] Analysis pipeline trivial — query Postgres directly with DuckDB / pandas / R / Excel
- [ ] HealthKit + Garmin paths require a separate native iOS app at v2 — deferred

### Storage

- [ ] Cloud-backed: PostgreSQL managed by Directus on Fly.io. TLS in transit, Postgres at-rest encryption per Fly.io defaults
- [ ] One entry per date (`date` is a UNIQUE constraint on `day_entries`; updates overwrite, never duplicate)
- [ ] Tags as references, not strings (so rename/merge is cheap)
- [ ] Schema includes collections for v1.5 / v2 data sources (`project_entries`, `garmin_daily`, `health_daily`, `weather_daily`, `calendar_events`) — left empty in v1 but present in the Directus instance
- [ ] All data exportable as CSV / JSON / Postgres dump (via Directus or direct Postgres access)

### Architecture readiness for v1.5 / v2

These items add **no v1 features** but prevent a future rewrite. Required in v1 even though unused:

- [ ] `projects`, `project_entries`, `project_field_configs` Directus collections defined (empty in v1)
- [ ] `calendar_events` Directus collection defined
- [ ] Tag category supports `project:<id>` and `custom`
- [ ] Data-source integrations designed as modules with a standard "fetch + aggregate + store per day" interface (no v1 modules implemented; structure must exist in `src/lib/integrations/`)
- [ ] Future native iOS app (if v2 HealthKit ambitions activate) queries the same Directus backend — no data migration needed

### Privacy

- [ ] No analytics, tracking, ads, telemetry
- [ ] No third-party SDKs that phone home
- [ ] Personal data never committed to the repo (this requirements doc, the brief, and the tech doc are the only artifacts that may reference personal context)
- [ ] All OAuth scopes (Google Calendar v1.5+) are minimal — `calendar.readonly` only
- [ ] Directus instance is single-admin (author), behind HTTPS only, with sane Fly.io defaults (Postgres encrypted at rest, automatic backups)

### Quality

- [ ] Works on the author's daily-driver iPhone (Safari + installed PWA)
- [ ] Daily flow tested under "tired user" conditions (no fiddly targets, no easy mis-taps)
- [ ] CSV import covers the existing 1.363-day dataset without manual cleanup
- [ ] Online-failure UX is graceful: clear "no network, retry" state on the daily screen

---

## Open questions (carry into prototype)

From the brief and tech doc:

1. ~~Final framework choice~~ — resolved: Next.js PWA + Directus. See [decisions/0002-pwa-with-directus-backend.md](decisions/0002-pwa-with-directus-backend.md). (Superseded [0001-framework-expo.md](decisions/0001-framework-expo.md).)
2. ~~Sync backend~~ — resolved by framework pivot: Directus + Postgres on Fly.io is the backend.
3. Progressive disclosure pattern for the daily screen — how blocks 2/3/4/5 reveal without cluttering Block 1.
4. ~~Minimum iOS version~~ — irrelevant for PWA; minimum browser version is "current Safari, Chrome, Firefox, Edge".
5. ~~Garmin Body Battery / Stress score path~~ — deferred: not addressable in PWA. Would require a separate native iOS app at v2.
6. **New**: Offline-cache + write-queue layer — add when real usage proves it's needed; deferred from v1.
7. **New**: Directus collection schema — to be modeled per [data-model.md](architecture/data-model.md). To be created in the new Directus instance once stood up.

These do **not** need to be resolved before prototyping v1, but should be flagged in any v1.5/v2 planning.

---

## Success criteria for v1

- The author replaces the Google Sheet with this app for daily logging within one week of v1 install
- Coverage stays at 100% (no skipped days because of app friction)
- Time-on-screen for a typical entry stays under 10 seconds
- 1.363-day history is importable and viewable in the timeline on first launch
