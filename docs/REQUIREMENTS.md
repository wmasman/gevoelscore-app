# Requirements — v1

Distilled from [app_brief_gevoelscore.md](app_brief_gevoelscore.md) and [technisch_document.md](technisch_document.md). This file is the short version. The two longer docs hold the reasoning and alternatives.

---

## Cardinal principles

These are hard constraints. A v1 that violates them is a failure regardless of feature count.

1. **One-tap entry**: a complete day requires one tap. Nothing else is mandatory.
2. **Sub-10-second goal**: open app, log score, optionally type a note, close. ≤ 10 seconds on a good day.
3. **No friction in the main flow**: dropdowns, sliders, required tags or multi-step forms on the daily screen are forbidden.
4. **Low cognitive load**: usable on a "4-out-of-6 day" with brainfog. No flashing colors, no unnecessary animations, no sound.
5. **No unsolicited notifications, ads, analytics, or tracking.** Reminders exist only as explicit user opt-in — the canonical example is the v2 end-of-day score reminder: off-by-default, silent, at most once per day, observational copy, never engagement-framed. Spec lives in [technisch_document.md](technisch_document.md#end-of-day-reminder) and the design tone is locked in [design/brief.md](design/brief.md#allowed-nuances).
6. **User-owned data**: data lives on infrastructure the author controls (self-hosted Directus + Postgres). No third-party telemetry, no data sold or shared. Full export and full delete are first-class features. _(Note: this principle changed from the original "local-first" framing when the architecture pivoted to cloud-backed — see [ADR 0002](decisions/0002-pwa-with-directus-backend.md).)_

---

## User requirements (v1)

### Must-have

- [ ] Log a daily score: integer 1–10 only (no halves, no decimals). Matches the original Google Sheet's 1–10 scale (the brief notes 7–10 were unused in the 1.363-day history, but the range stays open in case recovery patterns shift). Nuance still lives in `note` and tags. See [architecture/data-model.md](architecture/data-model.md) (DayEntry, "Score validation").
- [ ] Optional free-text note per day (no length limit)
- [ ] Optional chip-tags per day, multi-select
- [ ] Tag set is personal and dynamic: frequently used tags surface, rarely used tags fade
- [ ] Seed tag set in **five clusters** — supersedes the brief's original 4-cluster proposal (which lumped positive markers into a separate `positief` cluster; the new model treats valence as a value within each dimension rather than a separate axis):
  - **mentaal** — `brainfog`, `emotioneel`, `overprikkeld`, `stress`, `somber`, `helder`, `kalm`, `goede focus`
  - **fysiek** — `hoofdpijn`, `moe`, `zware benen`, `spierpijn`, `slecht geslapen`, `verkouden`, `koorts`, `misselijk`, `keelpijn`, `nekpijn`, `goede energie`, `goed geslapen`, `geen pijn`
  - **overall** — `rotdag`, `off`, `goede dag`, `lekker snel`, `top`
  - **activiteit** — what the user *did*: `rustdag`, `licht`, `matig`, `zwaar`, `wandeling`, `kantoor`, `sport`, `ademhalingsoefening`
  - **gebeurtenis** — what *happened* to the user: `verjaardag`, `afspraak_zorg`, `werkmeeting`, `reis`, `ziekenhuisbezoek`, `slecht nieuws`
- [ ] User can add, rename, archive and merge tags
- [ ] Timeline view: last 30 days and last 90 days, simple line chart
- [ ] Streak counter (consecutive days logged)
- [ ] Calendar view for backfill — empty days clearly marked, one tap to open
- [ ] **Recent-missed-days quick view** — a focused list of the last ~4–7 days showing which are empty, separate from the full calendar. Tap any day to enter or edit.
- [ ] **Today's entry: frictionless overwrite** — within the daily-entry session, the score saved at 09:00 can be overwritten at 16:00 with the same one-tap action. No confirmation dialog, no "are you sure"; the upsert-by-date contract handles it. The most recent tap wins.
- [ ] **Past-day edit: deliberate** — opening any past day shows the stored score / note / tags in **read-only** form. An explicit "Edit" affordance toggles edit mode; within edit mode, the same auto-save rule applies. This protects established data from accidental overwrites while keeping today's flow frictionless.
- [ ] **Auto-save** — every field change saves immediately. No "Save", "Submit", or "Done" button anywhere in the data-entry flow. The only "are you sure" moment is the past-day Edit toggle.
- [ ] **Login** — single-user account on the author's Directus instance. Email + password.
- [ ] **2FA (TOTP)** — required on every login. Uses Directus's built-in two-factor support (RFC 6238). Pairs with any standard authenticator app (Google Authenticator, Authy, 1Password, Bitwarden). Setup happens once via Directus admin or in-app on first login; recovery is admin-side (clear the TOTP secret in Directus, re-pair).
- [ ] Import existing 1.363-day Google Sheet (CSV/XLSX): column B → score, column C → note
- [ ] Export everything to CSV at any time
- [ ] Online-first (daily entry requires network connectivity; offline support is a v1.5+ feature, not a v1 requirement — see [ADR 0002](decisions/0002-pwa-with-directus-backend.md) for the deliberate scope shift)
- [ ] **Mobile-first UI/UX** — design for phone width first (375px reference), treat desktop as a derivative layout. No "desktop-first then squashed to mobile" patterns. One-handed phone use in bed is the primary context. Installable as PWA via "Add to Home Screen".

### v1 screens

These are the concrete screens v1 ships. Anything not on this list is out of scope for v1 unless explicitly justified.

| Screen | Purpose | Cardinal-principle role |
|--------|---------|--------------------------|
| **Login** | Email + password into Directus | Gatekeeper — must be fast (≤ 5s) so it doesn't add to the sub-10s budget |
| **2FA verify** | TOTP 6-digit code | Same — biometric autofill where possible to keep it fast |
| **2FA setup** | First-time TOTP pairing (QR + manual secret). Also reachable from Settings. | One-time flow; can take longer; not on the daily path |
| **Home / Daily** | The cardinal-principle screen: score buttons 1–10, free-text note, quick-tag chips for today | **This is the screen all rules are designed for.** Must hit one-tap entry, sub-10s, brainfog-friendly, auto-save. **UI design note:** 10 buttons on a 375px phone screen needs a layout decision — single row (small buttons, ~34px each), two rows of 5, or another pattern. Resolved in the Home/Daily feature plan, not here. |
| **Recent missed** | Last 4–7 days showing which are empty; tap to enter or open for edit | Backfill on the go — fast catch-up after a missed day |
| **Calendar** | Full backfill grid by month; tap any day to open | Deep backfill (e.g. a holiday week) |
| **Past-day view** | Read-only display of a stored day. Explicit "Edit" affordance toggles to edit mode (then auto-save). | Protects established data; the only "are you sure" moment |
| **Timeline** | 30-day / 90-day line chart + streak counter | Quick pattern-spotting. Not the dashboard — that's v1.5. |
| **Settings** | Tag management (add / rename / archive / merge), 2FA management, CSV import, CSV export, sign out | Infrequent flows; not on the daily path |

The **Past-day view** is most likely a screen-level route rather than a modal — it should be linkable from both the Calendar and the Recent-missed list. The Edit toggle is part of this screen, not a separate one.

### Out of scope for v1

- **Dashboard with richer trends** (v1.5) — Timeline + Streak cover v1. The brief's reference dashboard (`gevoelscore_analyse.html`: crash detection, energy envelope, intervention markers, seasonal effects) ships in v1.5 once daily entry is solid and there's real cloud data to chart.
- Projects / interventions tracking (v1.5)
- Google Calendar sync (v1.5)
- Apple Health, Garmin, weather data (v2)
- Sub-scores, end-of-day reminder, bonus fields (v2)
- Offline write queue (v1.5 if needed; v1 surfaces "no network, retry" per ADR 0002)
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

### Auth

- [ ] Directus email + password auth via the `@directus/sdk`. No homegrown crypto.
- [ ] **2FA via Directus's built-in TOTP** (RFC 6238). Enabled on the single user account; required on every login. Login flow handles the `INVALID_OTP` / `INVALID_OTP_REQUIRED` error path to prompt for the 6-digit code.
- [ ] Session via `httpOnly` + `Secure` + `SameSite=Strict` cookies, set by a Next.js Route Handler that proxies the Directus auth response. Browser code never sees the access token.
- [ ] Login + 2FA verify combined target ≤ 5 seconds on a good-day attempt — must stay outside the cardinal sub-10s daily-entry budget.
- [ ] CSRF protection: `SameSite=Strict` cookies + server-side Origin / Referer check on mutations, per [.claude/security-checklist.md](../.claude/security-checklist.md). No double-submit-cookie token plumbing.
- [ ] No forgot-password flow in v1 (single user; admin resets via Directus UI).

### Auto-save & data-write semantics

- [ ] Every field change in the daily-entry / edit-mode flow auto-saves immediately. Debounced where appropriate (e.g. 500ms after typing stops in the note field). No "Save" / "Submit" / "Done" button anywhere in the data-entry path.
- [ ] **Upsert by date** is the only write contract for `DayEntry`: PATCH if the date already has a row, INSERT otherwise. Single endpoint, idempotent.
- [ ] Subtle "saved" affordance (e.g. a fading checkmark) confirms each write. Errors surface as a toast with a Retry action; the unsaved change persists in the form until the retry succeeds.
- [ ] Past-day Edit toggle is the only friction point — read-only by default; explicit tap to enter edit mode; auto-save applies once inside edit mode.

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
