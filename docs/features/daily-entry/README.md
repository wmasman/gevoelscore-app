# Daily entry — Blok 1 (score) + Blok 2 (timeline)

**Feature:** The cardinal v1 product — one tap to log today's gevoelscore, optional note + tags, and a timeline that shows the patterns underneath. The audit-hardened auth layer is in place; this is what the auth was protecting.
**Version:** v1
**Status:** Planning 2026-05-27. Domain layer + Directus schema + 1,363 days of historical data already shipped.
**Parent docs:** [REQUIREMENTS.md](../../REQUIREMENTS.md), [app_brief_gevoelscore.md](../../app_brief_gevoelscore.md), [data-model.md](../../architecture/data-model.md), [queries-and-views.md](../../architecture/queries-and-views.md), [security-checklist](../../../.claude/security-checklist.md)

---

## Why this feature exists

The audit + auth + standards-enforcement work was all infrastructure. This is the product. The user has 1.363 days of daily-tracking evidence that this pattern works for them — one number plus optional context, viewed over time, surfaces what makes a good or bad Long COVID day. v1 ships that experience as a one-tap PWA so the daily ritual stays under 10 seconds even on brainfog days.

Cardinal principles this feature lives or dies by:

- **One tap entry**: a score-tap saves the day. Note + tags are optional, never required.
- **Sub-10-second flow**: open app → tap → done. 5s login budget separate.
- **Brainfog-friendly**: large targets, high contrast, no confirmations, no spinners that block the user, no "are you sure?" dialogs.
- **No telemetry**: no PostHog, no Sentry, no Vercel Analytics. ESLint rule enforces this.
- **User-owned data**: stays in the user's Directus on Fly + Neon. No third-party services touch it.

## What this feature ships

Two viewpoints — both live in the same single-page app, both gated behind the existing `/login` flow:

1. **Blok 1 — Today**: shows today's score (if logged) + a 1–10 tap row + optional note field + tag chips. The default state when the app opens.
2. **Blok 2 — Timeline**: a 30-day and 90-day chart of scores, plus a streak counter (consecutive days logged). Scrollable / swipeable to the Blok 1 view.

What's deliberately deferred (separate features later):

- **CSV import UI** — the parser ships, but the upload form is a follow-up (1.363 days are already imported via `directus/scripts/import-real-history.mjs`).
- **CSV export** — required by the cardinal "user-owned data" principle. Separate feature; not blocked by this one because the data is already exportable via Directus admin REST.
- **Delete-all** — same reasoning.
- **Tag management UI** (rename, archive, create) — 83 tags already seeded; v1 picks from those. New tag creation is a v1.5 nice-to-have.
- **Project tracking** (Blok 3) — schema is provisioned; UI is v1.5.
- **Sub-scores, sleep, weather, calendar** — schema is provisioned but the daily flow stays focused on the single score. v2.

## Acceptance criteria

**Blok 1 — Today (the daily tap):**

- [ ] AC1: Opening `/` shows today's entry if one exists for `YYYY-MM-DD` (browser's local date), or an empty score row if not.
- [ ] AC2: Tapping a score 1–10 immediately upserts the day_entry for today. No "save" button. No confirmation dialog.
- [ ] AC3: After tap, the UI reflects the saved state within 1s (optimistic update; reconciles with server response).
- [ ] AC4: Tap-to-change works: tapping a different number updates the existing entry.
- [ ] AC5: Note field is below the score. Free text, no length cap (matches data model). Saves on blur or after 1.5s of typing-pause (whichever first); never on every keystroke.
- [ ] AC6: Tag chips are below the note. The 83 seeded tags are grouped by category (mentaal/fysiek/overall/activiteit/gebeurtenis/interventie/project/custom). Tapping a chip toggles its inclusion; updates are upserted immediately.
- [ ] AC7: A score must be tapped *first* (in a fresh day with no entry). Note/tags edits to a non-existent day_entry create one with `score = null` is **not allowed** — the domain layer requires score 1–10. UI greys out note/tags until score is set.
- [ ] AC8: Network failure on save shows a small, non-blocking error ("Niet opgeslagen — probeer nogmaals") with a retry tap. Cardinal: brainfog-friendly = the failure mode is visible and obviously recoverable.
- [ ] AC9: The whole Blok 1 view fits on a phone screen without scrolling (touch targets ≥ 44px). Tested with one hand at arm's length in low light.
- [ ] AC10: Total flow on a good-day simulation (open app → tap 7 → close): ≤ 5 seconds, stopwatch-verified.

**Blok 2 — Timeline:**

- [ ] AC11: A swipe (or tap on a tab) reveals the timeline view. Default range: last 30 days.
- [ ] AC12: The chart shows a single line, x-axis = date, y-axis = score (1–10). Missing days are visible as gaps (no interpolation that lies about data).
- [ ] AC13: A toggle switches between 30-day and 90-day ranges. Loads from the server lazily — the 90-day view only fetches when first opened.
- [ ] AC14: Streak counter shows consecutive days logged (ending today or yesterday if today not yet logged). Resets visibly on a gap.
- [ ] AC15: Tapping a point on the chart shows that day's note + tags in a small bottom sheet. Tapping again or swiping down dismisses.
- [ ] AC16: Timeline accommodates the 1,363 days already in the database without performance degradation. The 90-day query reads ≤ 90 rows; 30-day reads ≤ 30. No client-side filtering of larger payloads.

**Auth + security:**

- [ ] AC17: All `/api/day-entries` routes require a valid session cookie (via `getValidatedSession`). Middleware already gates `/api/*` since step 7 of auth-hardening (M2 fix).
- [ ] AC18: Body validation on POST/PATCH uses domain-layer validators (`validateScore`, `validateNote`, `validateTagIds`, `validateDate`). Anything that doesn't pass returns 400 with a generic `invalid_request` — no field-by-field error leaks.
- [ ] AC19: Origin check on every state-changing route. Rate limit by IP at the standard 5/5min (creating 5 entries per 5 minutes per IP is plenty for a single user; abuse is the threat model).
- [ ] AC20: GET routes are not rate-limited (read traffic is the happy path; rate limiting reads on a single-user app is theatrical).

## Technical constraints

- **Domain layer is locked.** Routes consume the existing validators in [src/lib/domain/](../../../src/lib/domain/); no schema changes.
- **Directus schema is deployed.** The `day_entries`, `tags`, `day_entries_tags` collections exist and are populated. No `directus/scripts/` changes for v1.
- **No new dependencies.** The chart library and any state management are TBD per step file — but the bar is high: each new dep needs an ADR or rationale per the standards-enforcement table.
- **PWA shell** is in scope but not the *install* flow. The app should work as a website that happens to be installable; the prompt-to-install flow is post-v1.
- **Audit log INSERT placeholder**: every POST/PATCH/DELETE handler carries a `// TODO(I3): audit-log entry` comment for the future Track A3 backfill. No log infrastructure now (deferred to pre-launch).
- **Timeline performance**: 90 rows max per request. Use the existing `daily_observations` view if it lands first, or a direct Directus REST query otherwise. Decided per step file.

## Steps

1. **[Step 1 — `/api/day-entries` read API](step-1-day-entries-read-api.md)** — GET `/api/day-entries?from=X&to=Y` + GET `/api/day-entries/today`. Read-side first so the timeline can be hooked up to real historical data without any UI for writes yet.
2. **[Step 2 — Today screen shell](step-2-today-screen-shell.md)** — UI shows today's existing entry (read-only) with the 1,363 days as context. No tap-to-save yet. Establishes the page layout + auth-gated server component.
3. **[Step 3 — `/api/day-entries` write API](step-3-day-entries-write-api.md)** — POST + PATCH with upsert-by-date semantics. Origin check + rate limit + body validation per AC17–19.
4. **[Step 4 — Score-tap UI](step-4-score-tap-ui.md)** — Wire the 1–10 tap row to the write API. Optimistic update. AC1–AC4, AC8–AC10.
5. **[Step 5 — Note + tag chips UI](step-5-note-and-tags-ui.md)** — AC5–AC7. Tag picker uses the 83 seeded tags grouped by category.
6. **[Step 6 — Timeline (Blok 2)](step-6-timeline-blok2.md)** — Chart + streak counter. AC11–AC16. Decision point on chart lib lives here.

Each step follows the strict RED → GREEN → REFACTOR loop via `/build-step` with its own Done section. Each step file carries the standards-enforcement table per `/plan-feature` Phase 5.7.

## Verification

- **Automated**: Vitest grows from 380 to ~420 across the six steps (domain layer is already heavily tested; new tests are mostly route-handler + UI behaviour).
- **Playwright**: new specs under `tests/e2e/daily-entry.spec.ts` cover the score-tap happy path, the timeline swipe, and the offline-error path.
- **Live-stack**: new specs under `tests/live-stack/daily-entry.spec.ts` exercise the real Directus collection — verifies the row count matches the 1,363 baseline (read-only check) and that a write actually lands in Postgres.
- **Manual walkthrough** (cardinal-principle gate): one-handed, arm's length, low light, on the phone. Stopwatch the tap-to-score flow at ≤ 5s on a good-day simulation. Try a brainfog simulation (delay between intention and motor action — read but don't act for 2s — and verify the flow doesn't time out / require re-tapping). Run it on a network-throttled connection (Slow 3G in DevTools) to verify the optimistic update isn't blocking.

## Cardinal-principle impact

| Principle | Impact | How we stay inside |
|-----------|--------|--------------------|
| One-tap entry | This *is* the principle — score tap saves the day | No "save" button; no confirmation modal; one HTTP call |
| Sub-10-second flow | The thing that gets measured | Stopwatch at end of every step's walkthrough |
| Brainfog-friendly | Daily reality | ≥ 44px targets; high contrast; legible default font size; visible error state |
| No notifications / ads / analytics | Enforced | ESLint `no-restricted-imports` blocks Sentry/PostHog/Vercel Analytics |
| User-owned data | Directus on Fly + Neon | No third-party endpoints in the network panel |
| Export / delete still works | Deferred but unblocked | Schema unchanged; export endpoint can be added without touching this feature |

## Alternatives considered

### Decision: Upsert-by-date vs. POST-create / PATCH-update

- **Chose:** PUT `/api/day-entries/[date]` with upsert semantics — if the row exists, update; if not, create. Single endpoint, single client call.
- **Considered and rejected:** Separate POST (create) + PATCH (update) with the UI checking existence first. Adds a round-trip and a race condition window (user taps fast → two POSTs).

### Decision: Optimistic update vs. wait-for-server

- **Chose:** Optimistic. The UI reflects the tap immediately; reconciles with the server's `updated_at` when the response lands. On failure, the score reverts and an error toast appears.
- **Considered and rejected:** Spinner during save. Adds visible latency on every tap, kills the "one tap = done" feeling.

### Decision: Chart library

- **Deferred to Step 6** — the lightest option that handles 90 datapoints + missing-data gaps is the goal. Candidate set (no decision yet, all evaluated when Step 6 plans): vanilla SVG (no dep, ~50 LOC), Recharts (React-native, ~80kB), uPlot (smallest mature lib, ~40kB), Chart.js (heaviest). Decision goes in Step 6 with an ADR if it's a new dep.

## Privacy & permissions

- **No new data shapes.** Everything ships to existing `day_entries` + `day_entries_tags` collections under the existing `gevoelscore-frontend-api` role.
- **No third-party services touch the data.** No analytics, no error reporting, no CDN-served content involving the data.
- **Export / delete**: out of scope for this feature, but the schema is already export-friendly (Directus REST returns JSON; CSV is trivial). Tracked separately.

## Security

The audit findings the auth layer closed today (H1/H2/H4/M1 + M2/M3/M5/H3/L5) are all upstream of this feature. The specific items the daily-entry routes must respect:

- A01: every route requires a valid session via `getValidatedSession`.
- A03: body validation through domain validators + Zod (at least at the schema-shape level); no string-concat queries.
- A04: rate-limit writes at 5/5min by IP.
- A05: security headers (set globally in `next.config.ts`) apply to the daily-entry routes too.
- A08: origin check on every write; SameSite=Strict cookie already in place.
- A09: no PII in logs — the note field is free text and counts as PII; log only `{ outcome, ip-hashed }` per request, never the body.

## v1.5 / v2 readiness

- **Schema is forward-compatible**: `sub_scores`, `sleep_hours`, `special_event`, `garmin`, `health`, `weather`, `derived` are all already nullable columns. v2 features add data without touching v1 code.
- **Tag categories** are locked at 8 values; new categories require a schema migration (intentional friction).
- **Native iOS app** (v2 per ADR 0002): same Directus auth flow, same `/api/*` shape — the iOS app talks to the same Route Handlers. Nothing in this feature blocks that.

## What this feature does NOT do

- Does NOT add the CSV import UI (`directus/scripts/import-real-history.mjs` already did the bulk load; UI follows later).
- Does NOT add a CSV export endpoint (separate feature; required for v1 "user-owned data" gate but not blocked by daily-entry).
- Does NOT add a delete-all endpoint (same).
- Does NOT implement Blok 3 / projects (v1.5).
- Does NOT add the audit-log INSERTs (deferred to A3 / pre-launch; placeholder comments only).
- Does NOT install Next.js, Directus, or the frontend Directus user (all prereqs done).
- Does NOT implement service worker / offline-write queue (offline is v1.5+ per ADR 0002).
