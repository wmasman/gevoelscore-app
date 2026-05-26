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
6. **Local-first, user-owned data**: raw data never leaves the device without explicit, per-source opt-in.

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
- [ ] Works fully offline
- [ ] Mobile-first UI (designed for one-handed phone use in bed)

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

**Decision: Expo (React Native), managed workflow.** See [decisions/0001-framework-expo.md](decisions/0001-framework-expo.md) for the reasoning.

- [x] Mobile-first — Expo ships real native iOS/Android binaries
- [x] Offline-capable — `expo-sqlite` + local-first design
- [x] Path to HealthKit without rebuilding — `react-native-health` for most metrics, targeted Swift native modules for edge cases
- [x] Author's React/TypeScript stack — direct match
- [x] No Mac required — EAS Build for iOS, EAS Submit for App Store

### Storage

- [ ] Local-first with encrypted SQLite (SQLCipher or CryptoKit-backed)
- [ ] One entry per date (date is primary key; updates overwrite, never duplicate)
- [ ] Tags as references, not strings (so rename/merge is cheap)
- [ ] Schema includes nullable fields for v1.5 / v2 data sources (`project_entries`, `garmin`, `health`, `weather`, `calendar_events`) — left empty in v1 but present
- [ ] All data exportable as CSV / JSON / SQLite dump

### Architecture readiness for v1.5 / v2

These items add **no v1 features** but prevent a future rewrite. Required in v1 even though unused:

- [ ] `Project`, `ProjectEntry`, `ProjectFieldConfig` schemas defined (empty tables ok)
- [ ] `CalendarEvent` schema defined
- [ ] Tag category supports `project:<id>` and `custom`
- [ ] Data-source integrations designed as modules with a standard "fetch + aggregate + store per day" interface (no v1 modules implemented; structure must exist)
- [ ] Cloud sync strategy chosen on basis of the eventual passive-data load, not v1's needs

### Privacy

- [ ] No analytics, tracking, ads, telemetry
- [ ] No third-party SDKs that phone home
- [ ] Personal data never committed to the repo (this requirements doc, the brief and the tech doc are the only artifacts that may reference personal context)
- [ ] All HealthKit / OAuth scopes are per-type opt-in (deferred to v1.5+)

### Quality

- [ ] Works on the author's daily-driver iPhone
- [ ] Daily flow tested under "tired user" conditions (no fiddly targets, no easy mis-taps)
- [ ] CSV import covers the existing 1.363-day dataset without manual cleanup

---

## Open questions (carry into prototype)

From the brief and tech doc:

1. ~~Final framework choice~~ — resolved: Expo. See [decisions/0001-framework-expo.md](decisions/0001-framework-expo.md).
2. Sync backend: Supabase vs Firebase vs self-hosted Postgres (when v2 cloud sync is needed).
3. Progressive disclosure pattern for the daily screen — how blocks 2/3/4/5 reveal without cluttering Block 1.
4. Minimum iOS version: iOS 17+ enables `TimeInDaylight`; iOS 16+ enables sleep stages. Acceptable to require iOS 17?
5. Garmin Body Battery / Stress score path — only via Apple Health (lossy) or also a nightly Cloud Function fallback?

These do **not** need to be resolved before prototyping v1, but should be flagged in any v1.5/v2 planning.

---

## Success criteria for v1

- The author replaces the Google Sheet with this app for daily logging within one week of v1 install
- Coverage stays at 100% (no skipped days because of app friction)
- Time-on-screen for a typical entry stays under 10 seconds
- 1.363-day history is importable and viewable in the timeline on first launch
