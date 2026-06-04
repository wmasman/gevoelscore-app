# Step 1: Google OAuth + Settings + manual sync + Context tab

**Estimated time:** ~16 hours (the largest step in this feature). Combines: Google OAuth provider, three OAuth routes (connect/callback/disconnect), calendar-selection screen, manual `Ververs nu` path of the sync route, sync orchestrator, Settings → Kalenders surface, Context tab events section, per-event detail BottomSheet, sluit-uit and re-include flows (single + series), and the three smart-default rules applied at pull time.
**Test layers:** Vitest unit tests for the `GoogleCalendarProvider` (mock fetch to Google); Vitest unit tests for the sync orchestrator (mock provider); Vitest route tests for all six new routes (mirror the [merge-route auth-stack pattern](../../../src/app/api/tags/[id]/merge/route.ts)); Vitest component tests for `CalendarsSection`, `ChooseCalendarsForm`, `CalendarEventSheet`, `ContextEventsSection`; production smoke `scripts/calendar-binding-smoke.mjs` for the connect → sync → exclude round-trip.
**Risk:** High. First OAuth integration in the codebase; first encrypted-at-rest column. The combined-flow ACs (calendar selection + first sync) are the most fragile end-to-end path.
**Prerequisite:** Step 0 complete. `calendar_connections` / `calendar_events` / `calendar_series_exclusions` / `cron_monitor` collections live in production. `verify-schema` GREEN. `CALENDAR_KEK` Fly secret set. The `CalendarProvider` interface + canonical `CalendarEvent` + `computeDefaultIncluded` + `encrypt`/`decrypt` helpers exist and are GREEN. **`GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET` Fly secrets set** (admin-set in Google Cloud Console + Fly secrets manager before this step starts; setup procedure documented in step-1.0 below).

> Step-1 is large but cohesive — OAuth + Settings + Context all hang together. If during the build the integration surface exceeds capacity, the natural split point is **step-1a** (OAuth + Settings + sync route + sync orchestrator + 3 smart-default rules at pull time) and **step-1b** (Context tab + per-event sheet + tag/episode linking + sluit-uit + series-include). The split decision is made by the developer during the build; both halves test against the same set of ACs.

---

## Acceptance criteria (subset of feature README's criteria delivered by this step)

### Google provider implementation

- [ ] **AC1.1** `src/lib/integrations/google/google-provider.ts` exports `GoogleCalendarProvider` implementing `CalendarProvider` with `id = 'google'`. All 6 methods implemented.
- [ ] **AC1.2** `buildAuthUrl(state, redirectUri)` returns `https://accounts.google.com/o/oauth2/v2/auth?...` with: `client_id`, `redirect_uri`, `response_type=code`, `scope=https://www.googleapis.com/auth/calendar.readonly`, `access_type=offline`, `prompt=consent`, `state=<state>`. **No other scopes.**
- [ ] **AC1.3** `exchangeCode(code, redirectUri)` POSTs to `https://oauth2.googleapis.com/token` with `grant_type=authorization_code`. Returns `{ refreshToken, accessToken, expiresAt, accountEmail }`. Account email is read from the ID token claim (returned in the token response when `openid email` is requested — but to keep the scope minimal we read it from the calendar list's primary entry instead, fetched right after token exchange).
- [ ] **AC1.4** `refreshAccessToken(refreshToken)` POSTs to `https://oauth2.googleapis.com/token` with `grant_type=refresh_token`. Returns `{ accessToken, expiresAt }`. Caches in memory (request-scoped, not cross-request).
- [ ] **AC1.5** `listCalendars(accessToken)` GETs `https://www.googleapis.com/calendar/v3/users/me/calendarList?minAccessRole=reader`. Returns `Array<{ id, displayName, isPrimary }>`. Hides Google's "Holidays in NL" and "Contacts" calendars by default? **No** — surface them all; the user opts-in per calendar.
- [ ] **AC1.6** `fetchEvents(accessToken, includedCalendarIds, from, to)` iterates `includedCalendarIds`, fetching `https://www.googleapis.com/calendar/v3/calendars/{calendarId}/events?timeMin=...&timeMax=...&singleEvents=true&maxResults=2500&showDeleted=false`. Pages via `nextPageToken` if present. Maps Google's response shape to canonical `CalendarEvent`.
- [ ] **AC1.7** `fetchEvents` correctly populates `recurrenceId` from Google's `recurringEventId` field on instance events.
- [ ] **AC1.8** `fetchEvents` correctly populates `declined` by inspecting the `attendees[]` array for an entry where `self === true && responseStatus === 'declined'`.
- [ ] **AC1.9** `fetchEvents` correctly populates `allDay` when Google returns `start.date` (not `start.dateTime`).
- [ ] **AC1.10** `fetchEvents` correctly populates `attendeesCount` from `attendees.length` (0 if no attendees array).
- [ ] **AC1.11** `revoke(refreshToken)` POSTs to `https://oauth2.googleapis.com/revoke?token=<refreshToken>`. Returns void on success. Treats 200 AND 400 ("invalid_token", meaning already-revoked) as success. Anything else throws.
- [ ] **AC1.12** All Google-API responses are Zod-validated before being trusted. Schemas in `src/lib/validation/calendar-binding.ts`. Invalid responses throw with `google_api_invalid_response`.

### Sync orchestrator

- [ ] **AC1.13** `src/lib/sync/calendar-sync.ts` exports `syncConnection(accessToken: string, connection: DirectusCalendarConnectionRow, provider: CalendarProvider, now: Date): Promise<SyncResult>` where `SyncResult = { connectionId, eventsPulled, eventsUpserted, eventsExcludedBySeries, errors: string[] }`.
- [ ] **AC1.14** Sync window: `from = now - 7 days`, `to = now + 30 days`. Constants in `src/lib/sync/calendar-sync.ts` exported as `SYNC_WINDOW_BACK_DAYS = 7` and `SYNC_WINDOW_FORWARD_DAYS = 30`.
- [ ] **AC1.15** Refreshes the access token via `provider.refreshAccessToken` using the decrypted refresh token from the connection row. If refresh fails, surfaces `refresh_token_invalid` error and updates `connection.last_sync_error` + `status='error'`.
- [ ] **AC1.16** Fetches events via `provider.fetchEvents(accessToken, connection.included_calendar_ids, from, to)`.
- [ ] **AC1.17** Loads existing series exclusions for the connection: `readItems('calendar_series_exclusions', { filter: { connection_id: { _eq: connection.id } } })`. Builds a `Set<recurrence_id>`.
- [ ] **AC1.18** For each fetched event, computes `included_as_context` + `reason` via `computeDefaultIncluded(event, seriesExclusionSet)` from step-0.
- [ ] **AC1.19** Upserts via `createItems` for new events (ON CONFLICT by UNIQUE(connection_id, provider_event_id) → `updateItems`). The Directus SDK doesn't expose true upsert; the orchestrator does a `readItems` for existing provider_event_ids + diff, then bulk creates / patches. **Bulk operations:** one `createItems` for inserts, one `updateItems` per changed-field-shape for updates (typically one or two batches).
- [ ] **AC1.20** New events get `user_decision = 'auto'`. Existing events keep their `user_decision` (the user's prior override sticks across re-syncs).
- [ ] **AC1.21** Events whose `recurrenceId` matches a row in `calendar_series_exclusions` get `included_as_context = false` AND `user_decision = 'user_excluded'` on insert (so the series rule keeps applying to future fresh pulls). On update of an existing series-excluded event, `user_decision` stays `'user_excluded'`.
- [ ] **AC1.22** After the upsert, updates `connection.last_synced_at = now`, `last_sync_error = NULL`, `status = 'active'`.
- [ ] **AC1.23** Errors during fetch don't break the whole sync. Each connection's sync is independent; one connection's `refresh_token_invalid` doesn't prevent another's success.

### Route: connect

- [ ] **AC1.24** `POST /api/calendars/google/connect` — standard auth stack: origin → session → rate-limit (existing `tagWriteRateLimiter` reused for write-shape consistency; budget unchanged at 200/5min — connect is far rarer than tag writes but the same limiter is fine).
- [ ] **AC1.25** Generates a cryptographically random `state` (32 bytes base64url). Sets a signed cookie `cal_oauth_state` with `httpOnly` + `Secure` + `SameSite=Lax` (Lax required for the OAuth redirect-back path) + 10-minute Max-Age.
- [ ] **AC1.26** Returns `{ redirect_url }` so the client can `window.location = url`. Alternative: route returns 302 to Google directly. **Chose:** JSON-with-redirect-url so the client controls the redirect (consistent with the rest of the app's POST patterns; the merge route returns JSON, not 302).

### Route: callback

- [ ] **AC1.27** `GET /api/calendars/google/callback?code=...&state=...` — origin check (no body, no rate-limit; the callback is a GET).
- [ ] **AC1.28** Validates `state` query param against `cal_oauth_state` cookie. Mismatch → 400 `state_mismatch`. Missing cookie → 400 `state_missing`.
- [ ] **AC1.29** Validates session (the user must have been logged in when they started the connect flow).
- [ ] **AC1.30** Exchanges `code` for tokens via `provider.exchangeCode`. Lists calendars to get the primary calendar's email (`accountEmail`).
- [ ] **AC1.31** Encrypts the refresh token via `encrypt(refreshToken, env.CALENDAR_KEK)`.
- [ ] **AC1.32** Inserts or updates a `calendar_connections` row with `(user_id, provider='google', provider_account_email, refresh_token_encrypted, scope, connected_at=now, status='active', included_calendar_ids=[]`). Idempotent on `UNIQUE(user_id, provider, provider_account_email)` (UPDATE if row exists, INSERT if new).
- [ ] **AC1.33** Redirects (302) to `/settings/kalenders/choose?connection_id=<id>` so the user picks which calendars to include.

### Route: choose calendars

- [ ] **AC1.34** `GET /api/calendars/[connection_id]/calendars` — returns the list of calendars from Google for the given connection. Origin → session → ownership gate (the connection's `user_id` must match the session's user_id).
- [ ] **AC1.35** `POST /api/calendars/[connection_id]/calendars` — body: `{ included_calendar_ids: string[] }`. Validates each id is a string (Google calendar IDs are not UUIDs; can be email addresses or `addressbook#contacts@group.v.calendar.google.com`-style strings). Persists to `calendar_connections.included_calendar_ids`. Then triggers one immediate sync (calls `syncConnection`) so the Context tab is populated right away.

### Route: sync (manual path — bearer path lands in step-2)

- [ ] **AC1.36** `POST /api/calendars/sync` — accepts session auth (manual `Ververs nu`) OR bearer auth (step-2 cron, gated behind `CALENDAR_SYNC_SECRET`). In step-1, only the session path is wired; the bearer gate code is present and tested but step-1 doesn't ship the cron workflow.
- [ ] **AC1.37** Session path: origin → session → rate-limit. Iterates all active connections for the session's user_id (in single-user v1.6, that's at most one; the code handles N).
- [ ] **AC1.38** Bearer path: matches `Authorization: Bearer <CALENDAR_SYNC_SECRET>` (constant-time comparison via `crypto.timingSafeEqual`). Iterates **all** active connections (not user-scoped — the cron is the system, not a user).
- [ ] **AC1.39** Both paths: for each connection, decrypts the refresh token, calls `syncConnection`, aggregates `SyncResult`. Returns `200 { connections: N, events_pulled: M, events_upserted: K }`.
- [ ] **AC1.40** Sync errors per-connection don't fail the route. Aggregate result includes per-connection error code if applicable.

### Route: disconnect

- [ ] **AC1.41** `POST /api/calendars/[connection_id]/disconnect` — origin → session → rate-limit → ownership gate.
- [ ] **AC1.42** Order: (1) call `provider.revoke(refreshToken)` (best-effort; idempotent on Google's side — 400 invalid_token is treated as success), (2) DELETE the `calendar_connections` row (cascade triggers DELETE on `calendar_events` + `calendar_series_exclusions` via FK ON DELETE CASCADE from step-0).
- [ ] **AC1.43** Revoke failure (other than the idempotent 400) is logged but does NOT prevent local cascade. The local row is deleted regardless. Surfaces `revoke_failed_but_local_cascaded` in the response so the user knows to manually revoke at https://myaccount.google.com/permissions if it matters.

### Route: per-event update

- [ ] **AC1.44** `PATCH /api/calendars/events/[id]` — origin → session → rate-limit → ownership gate (event's connection.user_id matches session.user_id). Accepts a JSON body with one or more of: `linked_tag_id` (UUID or null), `linked_episode_id` (UUID or null), `included_as_context` (bool).
- [ ] **AC1.45** If `included_as_context = false` is sent for a recurring event, the route inserts into `calendar_series_exclusions(connection_id, recurrence_id)` (idempotent on UNIQUE) AND bulk-updates all sibling events with that `recurrence_id` to `included_as_context = false` + `user_decision = 'user_excluded'`. Single round-trip from the client; multiple Directus writes server-side, ordered: INSERT exclusion → bulk PATCH siblings.
- [ ] **AC1.46** If `included_as_context = false` is sent for a non-recurring event, the route updates just that event to `included_as_context = false` + `user_decision = 'user_excluded'`. No series_exclusions row.
- [ ] **AC1.47** If `included_as_context = true` is sent for a recurring event, the route does NOT delete the series exclusion (asymmetric: re-include is per-event by default). Updates just that event to `included_as_context = true` + `user_decision = 'user_included'`. Series exclusion stays; future pulls of the recurrence still default to excluded.
- [ ] **AC1.48** If `included_as_context = true` is sent for a non-recurring event, updates just that event.
- [ ] **AC1.49** Returns `200 { id, linked_tag_id, linked_episode_id, included_as_context, user_decision }`.

### Route: series include (the symmetric coarse-include)

- [ ] **AC1.50** `POST /api/calendars/events/[id]/include-series` — origin → session → rate-limit → ownership gate. Path-id resolves to a recurring event; route uses its `recurrence_id` to DELETE the matching `calendar_series_exclusions` row AND bulk-update all sibling events to `included_as_context = true` + `user_decision = 'user_included'`.
- [ ] **AC1.51** If the event is non-recurring, returns 400 `event_not_recurring`. (The UI doesn't show this button on non-recurring events; defensive check.)
- [ ] **AC1.52** Returns `200 { recurrence_id, events_updated: N }`.

### Settings UI: Kalenders surface

- [ ] **AC1.53** `src/components/calendars-section.tsx` rendered inside the existing Settings view, **above** the existing Tag-beheer section (calendars is a setup step; tag-beheer is a cleanup activity). Empty state: `Geen kalenders verbonden` + `[Verbind Google Calendar]` button. Connected state: list of connections with email + last sync + `[Ververs nu]` + `[Ontkoppel]`.
- [ ] **AC1.54** `[Verbind Google Calendar]` button POSTs to `/api/calendars/google/connect`, then redirects the browser to the returned `redirect_url`.
- [ ] **AC1.55** `[Ververs nu]` button POSTs to `/api/calendars/sync` (session path). Shows `Synchroniseren...` while in flight, updates the last-sync time on success, surfaces error toast on failure.
- [ ] **AC1.56** `[Ontkoppel]` opens a confirm dialog (`role="alertdialog"` per the brainfog focus-on-Annuleer pattern from v1.5b). On confirm, POSTs to `/api/calendars/[connection_id]/disconnect`. On success, the row is removed from the Settings list and from all event surfaces (the cascade in step-0 handles the data).
- [ ] **AC1.57** No em-dashes anywhere in the Kalenders copy (per memory).

### Settings UI: choose calendars screen

- [ ] **AC1.58** `src/components/choose-calendars-form.tsx` renders the list of calendars from `GET /api/calendars/[connection_id]/calendars`. Each row: checkbox + display name + primary badge (if isPrimary). All checked by default.
- [ ] **AC1.59** `[Verbinden]` submit POSTs the checked ids to `POST /api/calendars/[connection_id]/calendars`. On success: redirect to `/settings#calendars`.
- [ ] **AC1.60** `[Annuleer]` cancels the connect flow. The `calendar_connections` row already exists (it was created in the callback); cancelling means included_calendar_ids stays `[]` (empty). The user can come back later via Settings and complete the selection. Alternative: cancelling deletes the connection row + revokes the grant. **Chose** the keep-row approach because (a) the user might want to retry the selection with different choices, (b) the empty included_calendar_ids means no events will be pulled, so it's safe.

### Context tab: events section

- [ ] **AC1.61** `src/components/context-events-section.tsx` rendered inside the existing Context tab view, above the existing Periodes section. Shows events overlapping the selected date where `included_as_context = true`, sorted by start_at ascending, all-day events first.
- [ ] **AC1.62** Each row: time (`HH:mm` for timed, `Hele dag` for all-day) + title + optional location + optional linked-tag badge + optional linked-episode badge. Recurring events show a small recurrence icon at the right edge.
- [ ] **AC1.63** Empty state (no events for the date): no section rendered. Empty space is fine; no copy needed.
- [ ] **AC1.64** `Toon overgeslagen events` toggle at the top of the section (matches the `Toon gearchiveerd` pattern from v1.5b tag-management). When ON: also renders events where `included_as_context = false` with reduced opacity + `(overgeslagen)` suffix.
- [ ] **AC1.65** Tap any event row → opens `CalendarEventSheet` (a nested BottomSheet).

### Context tab: per-event detail BottomSheet

- [ ] **AC1.66** `src/components/calendar-event-sheet.tsx` opens as a BottomSheet over the parent view. Closes on drag-down / Escape / tap-outside. Auto-saves each field change (no Save button); refreshes parent on close.
- [ ] **AC1.67** Top section: title (read-only, from `event.title`), full datetime (read-only), location (read-only).
- [ ] **AC1.68** Linked tag picker: tap "Koppel aan tag" → opens nested tag-picker sheet (re-uses `TagPickerSheet` from verloop-and-episodes step-5 if compatible; if not, a slimmed-down variant). Categories `interventie / activiteit / project / gebeurtenis` shown at top (these are the most-likely-linked categories for events). Pick a tag → PATCH `/api/calendars/events/[id]` with `linked_tag_id`. To unlink, the picker has a `[Geen]` option at the top.
- [ ] **AC1.69** Linked episode picker: tap "Koppel aan periode" → opens nested episode-picker. Lists non-archived episodes sorted by start_date desc. Pick → PATCH with `linked_episode_id`. `[Geen]` option to unlink.
- [ ] **AC1.70** `[Sluit uit als context]` button — single tap, no modal. For non-recurring events: PATCH with `included_as_context = false`. For recurring events: same PATCH; the route applies the series rule.
- [ ] **AC1.71** If the event is currently EXCLUDED (`included_as_context = false`), the button instead shows `[Weer meenemen]` (per-event re-include) AND for recurring events, an additional `[Voeg hele serie weer toe]` button below. The first POSTs to `/api/calendars/events/[id]` with `included_as_context = true`. The second POSTs to `/api/calendars/events/[id]/include-series`.
- [ ] **AC1.72** Sheet closes after the exclusion action (single tap → immediate feedback via parent re-render).

### Cross-feature integrity

- [ ] **AC1.73** **Daily flow UNCHANGED.** `QuickEntryFlow` / score-only path tap-count unaffected. Verified by re-running the existing daily-entry integration tests after step-1 changes.
- [ ] **AC1.74** **Tag picker UNCHANGED.** `TagCategoryList` inside `QuickEntryFlow` keeps working; linking a tag from an event sheet does NOT add the tag to today's day_entry (it links the tag to the event, not to the user's day).
- [ ] **AC1.75** **Episode picker UNCHANGED.** The episode-side `TagPickerSheet` from step-5 of verloop-and-episodes is unaffected; we either reuse it (preferred) or fork a slimmer variant for event-linking (acceptable). Decision in build.

### Privacy / logging

- [ ] **AC1.76** No event title, location, or attendee data appears in server logs (route logs, sync orchestrator logs, route error responses). Counts and provider_event_ids only.
- [ ] **AC1.77** OAuth state cookie is signed with `SESSION_SECRET` and is `httpOnly` + `Secure` + `SameSite=Lax` (Lax required for the OAuth redirect-back to set/read the cookie). 10-minute Max-Age.
- [ ] **AC1.78** Refresh tokens NEVER appear in logs or error responses. The encrypt helper from step-0 is the only path that touches the plaintext refresh token; everywhere else it's the encrypted blob.

---

## Technical constraints (applicable to this step)

- **OAuth redirect URI tightly allowlisted at Google.** Exactly `https://gevoelscore-frontend.fly.dev/api/calendars/google/callback` + `http://localhost:3000/api/calendars/google/callback` (dev only). Setup procedure documented in step-1.0 below.
- **State cookie is `SameSite=Lax`**, not `Strict`. Required for the OAuth redirect-back to read the cookie (Strict would block cross-site GET reads even from the same registrable domain on first navigation).
- **Bearer-gate code lands here but cron workflow lands in step-2.** The route accepts both auth shapes from step-1; tests cover both. The GHA workflow that exercises the bearer path is step-2.
- **Sync orchestrator is independent of route auth.** Same `syncConnection` called from manual (session) + cron (bearer). Tests mock the provider; production smoke tests the real Google path.
- **No keyword stoplist.** Confirmed in step-0 `computeDefaultIncluded`; step-1 just calls it.
- **Series-default exclusion is enforced by the route, not the orchestrator.** The route receives `included_as_context = false` and decides whether to insert a series_exclusion row based on whether the event is recurring. The orchestrator only applies existing exclusions on fresh pulls.
- **Re-include is per-row by default; series re-include is a separate explicit action.** Two routes: `PATCH /api/calendars/events/[id]` (per-row), `POST /api/calendars/events/[id]/include-series` (series).
- **`useEffect`-based polling is forbidden.** Manual `Ververs nu` is the only client-initiated sync. The Context tab does NOT auto-refresh on focus or interval.
- **No new external runtime deps for OAuth.** The flow is implemented with built-in `fetch` + `crypto`. No `googleapis`, no `next-auth`, no `@google-cloud/local-auth`. Smaller bundle + smaller supply chain.
- **All-day events stored as `start_at` = local midnight, `end_at` = next-day local midnight.** Google's `start.date` (no time) is interpreted in the user's timezone (assumed Europe/Amsterdam for v1.6 single-user; future multi-user will need a per-user timezone column). UTC storage with a documented timezone interpretation.
- **Sync window is 7 back / 30 forward.** Old events older than 7 days that exist in the DB stay (the cleanup of historical events is out of scope for v1.6).

### Standards-enforcement declaration

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01, A03, A04, A07, A08 | Yes | 6 new routes, all gated by origin + session/bearer + rate-limit + UUID-path + body Zod. Pattern mirrors merge-route. |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | Yes (writes) | `calendar_connections.refresh_token_encrypted` is encrypted. Other PII (event titles, attendees) is encrypted at rest by Fly Postgres LUKS. Export coverage: events YES, refresh tokens NO. Retention: cascade on Ontkoppel + full-delete. Audit logs: `created_at` + `connected_at` + `last_synced_at` are the audit trail. |
| New dependency | ADR or step rationale | No | Built-in `fetch` + `crypto` only. No `googleapis` SDK. |
| `dangerouslySetInnerHTML` usage | A03 | No | All UI uses text rendering. |
| New env var with a secret | A02, A05 | Yes | `GOOGLE_CLIENT_ID` (not really secret but Fly env), `GOOGLE_CLIENT_SECRET` (Fly secret), `CALENDAR_SYNC_SECRET` (Fly + GHA secret — set in step-2 but the route reads it). NEVER `NEXT_PUBLIC_*`. |
| New telemetry / observability dep | Cardinal "no telemetry" | No | None. |

---

## Test plan

The complete test enumeration. Test code paste-ready for the new files; for routes, the auth-stack tests are identical to the merge route pattern — see [src/app/api/tags/[id]/merge/__tests__/route.test.ts](../../../src/app/api/tags/[id]/merge/__tests__/route.test.ts) for the reference.

### Google provider (mock fetch to Google)

**File**: `src/lib/integrations/google/__tests__/google-provider.test.ts`

Tests (one `it` per AC):

1. `buildAuthUrl` includes `scope=https://www.googleapis.com/auth/calendar.readonly` and `access_type=offline` and `prompt=consent` (AC1.2)
2. `buildAuthUrl` does NOT include any other Google scope (AC1.2)
3. `exchangeCode` POSTs to `oauth2.googleapis.com/token` with `grant_type=authorization_code` (AC1.3)
4. `exchangeCode` returns `{ refreshToken, accessToken, expiresAt, accountEmail }` shape (AC1.3)
5. `exchangeCode` rejects malformed Google response with `google_api_invalid_response` (AC1.3, AC1.12)
6. `refreshAccessToken` POSTs with `grant_type=refresh_token` (AC1.4)
7. `refreshAccessToken` returns `{ accessToken, expiresAt }` (AC1.4)
8. `refreshAccessToken` surfaces `refresh_token_invalid` on 400 invalid_grant (AC1.4)
9. `listCalendars` GETs calendarList endpoint (AC1.5)
10. `listCalendars` maps `{ id, summary, primary }` → `{ id, displayName, isPrimary }` (AC1.5)
11. `listCalendars` surfaces holidays + contacts + birthdays calendars (no filter) (AC1.5)
12. `fetchEvents` iterates `includedCalendarIds`, one GET per calendar (AC1.6)
13. `fetchEvents` passes `timeMin` + `timeMax` + `singleEvents=true` + `maxResults=2500` + `showDeleted=false` (AC1.6)
14. `fetchEvents` follows `nextPageToken` until exhausted (AC1.6)
15. `fetchEvents` populates `recurrenceId` from `recurringEventId` (AC1.7)
16. `fetchEvents` populates `declined = true` when attendee `self === true && responseStatus === 'declined'` (AC1.8)
17. `fetchEvents` populates `declined = false` when no attendees array (AC1.8)
18. `fetchEvents` populates `allDay = true` when `start.date` present (no time) (AC1.9)
19. `fetchEvents` populates `allDay = false` when `start.dateTime` present (AC1.9)
20. `fetchEvents` populates `attendeesCount` from `attendees.length` (AC1.10)
21. `fetchEvents` populates `attendeesCount = 0` when no attendees array (AC1.10)
22. `fetchEvents` rejects malformed event with `google_api_invalid_response` (AC1.12)
23. `revoke` POSTs to `oauth2.googleapis.com/revoke?token=...` (AC1.11)
24. `revoke` treats 200 as success (AC1.11)
25. `revoke` treats 400 `invalid_token` as success (idempotent) (AC1.11)
26. `revoke` throws on 500 (AC1.11)

### Sync orchestrator

**File**: `src/lib/sync/__tests__/calendar-sync.test.ts`

Tests:

27. `syncConnection` uses `SYNC_WINDOW_BACK_DAYS = 7` and `SYNC_WINDOW_FORWARD_DAYS = 30` (AC1.14)
28. `syncConnection` calls `provider.refreshAccessToken` with decrypted refresh token (AC1.15)
29. `syncConnection` surfaces `refresh_token_invalid` + sets `connection.status = 'error'` on refresh failure (AC1.15)
30. `syncConnection` calls `provider.fetchEvents` with `included_calendar_ids` from connection (AC1.16)
31. `syncConnection` reads `calendar_series_exclusions` for the connection (AC1.17)
32. `syncConnection` applies `computeDefaultIncluded` to each fetched event (AC1.18)
33. `syncConnection` upserts new events with `user_decision = 'auto'` (AC1.19, AC1.20)
34. `syncConnection` upserts existing events preserving their `user_decision` (AC1.20)
35. `syncConnection` upserts events under existing series exclusion with `included_as_context = false` AND `user_decision = 'user_excluded'` (AC1.21)
36. `syncConnection` updates `last_synced_at = now`, `last_sync_error = NULL`, `status = 'active'` on success (AC1.22)
37. `syncConnection` records `last_sync_error` + sets `status = 'error'` on partial failure (AC1.23)

### Route: connect

**File**: `src/app/api/calendars/google/connect/__tests__/route.test.ts`

Tests (mirror merge-route auth-stack pattern):

38. 403 on bad origin
39. 401 without session
40. 429 on rate-limit
41. 200 with `redirect_url` and `cal_oauth_state` cookie set on success (AC1.25, AC1.26)
42. `redirect_url` contains the OAuth `state` param matching the cookie (AC1.25)
43. cookie has `httpOnly=true`, `Secure=true`, `SameSite=Lax`, `Max-Age=600` (AC1.77)

### Route: callback

**File**: `src/app/api/calendars/google/callback/__tests__/route.test.ts`

Tests:

44. 400 `state_mismatch` when query state doesn't match cookie (AC1.28)
45. 400 `state_missing` when cookie absent (AC1.28)
46. 401 without session (AC1.29)
47. 302 to `/settings/kalenders/choose?connection_id=<id>` on success (AC1.33)
48. `calendar_connections` row inserted with encrypted refresh token (AC1.31, AC1.32)
49. Second connect (same email) UPDATEs the existing row, doesn't INSERT (AC1.32; idempotent on UNIQUE)
50. Refresh token encryption is non-deterministic (different runs → different ciphertext) (AC1.31)

### Route: choose calendars (GET + POST)

**File**: `src/app/api/calendars/[connection_id]/calendars/__tests__/route.test.ts`

Tests:

51. GET 403 on ownership mismatch
52. GET 200 returns calendars from Google (AC1.34)
53. POST 400 on non-array body
54. POST 400 on non-string element in array
55. POST 200 persists `included_calendar_ids` (AC1.35)
56. POST triggers immediate `syncConnection` after persisting (AC1.35)

### Route: sync (session path)

**File**: `src/app/api/calendars/sync/__tests__/route.test.ts`

Tests:

57. 403 on bad origin (session path)
58. 401 without session and no bearer
59. 401 with invalid bearer (constant-time fail)
60. Session path: 200 aggregates results across active connections for the session user (AC1.37, AC1.39)
61. Bearer path: 200 aggregates across ALL active connections (AC1.38, AC1.39)
62. Per-connection error doesn't break the response; aggregate result includes the error code (AC1.40)
63. Bearer-gate uses `crypto.timingSafeEqual` (test via length-mismatch and per-byte timing — soft check via assertion that the comparison function is invoked)

### Route: disconnect

**File**: `src/app/api/calendars/[connection_id]/disconnect/__tests__/route.test.ts`

Tests:

64. 403 on ownership mismatch
65. 200 calls `provider.revoke` (AC1.42)
66. 200 deletes the connection row (cascade triggers events + series_exclusions delete) (AC1.42)
67. Revoke failure (500 from Google) → local cascade still runs; response includes `revoke_failed_but_local_cascaded` (AC1.43)
68. Revoke "already revoked" (400 invalid_token) → treated as success (AC1.42; idempotent)

### Route: per-event update

**File**: `src/app/api/calendars/events/[id]/__tests__/route.test.ts`

Tests:

69. 403 on ownership mismatch (event's connection.user_id ≠ session.user_id)
70. PATCH `linked_tag_id` updates the row (AC1.44)
71. PATCH `linked_episode_id` updates the row (AC1.44)
72. PATCH `included_as_context = false` on non-recurring event → just that event updated (AC1.46)
73. PATCH `included_as_context = false` on recurring event → INSERT into series_exclusions + bulk PATCH all siblings (AC1.45)
74. PATCH `included_as_context = false` on recurring event whose series is ALREADY excluded → INSERT is idempotent (UNIQUE), bulk PATCH is no-op (AC1.45)
75. PATCH `included_as_context = true` on recurring event → does NOT delete series_exclusion (asymmetric re-include) (AC1.47)
76. PATCH `included_as_context = true` on non-recurring event → just that event updated (AC1.48)
77. User_decision flips correctly: auto → user_excluded on toggle-off, → user_included on toggle-on (AC1.45, AC1.47)
78. Bulk PATCH order: INSERT exclusion BEFORE bulk PATCH siblings (so the exclusion is durable even if the bulk fails) (AC1.45)
79. Returns 200 with full updated event shape (AC1.49)

### Route: series include

**File**: `src/app/api/calendars/events/[id]/include-series/__tests__/route.test.ts`

Tests:

80. 403 on ownership mismatch
81. 400 `event_not_recurring` if path-id resolves to a non-recurring event (AC1.51)
82. 200 DELETEs the series_exclusions row + bulk PATCHes all siblings to included + user_decision = user_included (AC1.50)
83. Returns 200 with `recurrence_id` and `events_updated` count (AC1.52)
84. Order: DELETE exclusion BEFORE bulk PATCH (so the rule is gone first; bulk PATCH is then idempotent against re-applying) (AC1.50)

### Component: CalendarsSection (Settings)

**File**: `src/components/__tests__/calendars-section.test.tsx`

Tests:

85. Empty state renders `Geen kalenders verbonden` + `[Verbind Google Calendar]` (AC1.53)
86. Connected state shows email + last-sync time + Ververs/Ontkoppel buttons (AC1.53)
87. `[Verbind]` POSTs to /api/calendars/google/connect, then sets window.location to the returned redirect_url (AC1.54)
88. `[Ververs nu]` POSTs to /api/calendars/sync, shows in-flight state, updates last-sync time on success (AC1.55)
89. `[Ververs nu]` error → toast surfaces (AC1.55)
90. `[Ontkoppel]` opens alertdialog with focus on Annuleer (AC1.56)
91. `[Ontkoppel]` confirm POSTs to disconnect route (AC1.56)
92. No em-dashes in any copy (regex check on test output) (AC1.57)

### Component: ChooseCalendarsForm

**File**: `src/components/__tests__/choose-calendars-form.test.tsx`

Tests:

93. Renders list of calendars from API (AC1.58)
94. All checkboxes checked by default (AC1.58)
95. Primary calendar has a "Hoofd" badge (AC1.58)
96. Submit POSTs checked ids to POST route (AC1.59)
97. Submit redirects to /settings#calendars on success (AC1.59)
98. Annuleer returns to /settings#calendars without changing included_calendar_ids (AC1.60)

### Component: CalendarEventSheet

**File**: `src/components/__tests__/calendar-event-sheet.test.tsx`

Tests:

99. Renders title + datetime + location as read-only (AC1.67)
100. `[Koppel aan tag]` opens nested picker (AC1.68)
101. Picking a tag PATCHes /api/calendars/events/[id] with linked_tag_id (AC1.68)
102. `[Geen]` in tag picker unlinks (AC1.68)
103. `[Koppel aan periode]` opens episode picker (AC1.69)
104. Picking an episode PATCHes with linked_episode_id (AC1.69)
105. `[Sluit uit als context]` on non-recurring PATCHes included_as_context=false (AC1.70, AC1.46)
106. `[Sluit uit als context]` on recurring PATCHes (route applies series rule) (AC1.70, AC1.45)
107. Excluded event shows `[Weer meenemen]` + recurring shows additional `[Voeg hele serie weer toe]` (AC1.71)
108. `[Weer meenemen]` PATCHes included_as_context=true (per-row) (AC1.71)
109. `[Voeg hele serie weer toe]` POSTs to include-series route (AC1.71)
110. Sheet closes after exclusion action and parent refreshes (AC1.72)
111. No em-dashes in any copy (AC1.57)

### Component: ContextEventsSection

**File**: `src/components/__tests__/context-events-section.test.tsx`

Tests:

112. Renders events overlapping the selected date with included_as_context=true (AC1.61)
113. Sorts by start_at ascending (AC1.61)
114. All-day events render first (AC1.61)
115. Each row shows time (HH:mm) or `Hele dag` + title + optional location + tag/episode badges (AC1.62)
116. Recurring events show a recurrence icon at the right edge (AC1.62)
117. Empty state: section is not rendered (AC1.63)
118. `Toon overgeslagen events` toggle reveals excluded events with reduced opacity (AC1.64)
119. Tap event row opens CalendarEventSheet (AC1.65)

### Production smoke

**File**: `scripts/calendar-binding-smoke.mjs`

End-to-end against production:

1. Manual setup precondition: a fresh Google account with at least 1 calendar + 1 recurring event + 1 non-recurring event + 1 declined-RSVP event + 1 all-day event.
2. Connect: POST /api/calendars/google/connect, follow redirect (manual auth in browser; smoke pauses for user to complete OAuth).
3. Choose: POST /api/calendars/[id]/calendars with one calendar id (primary).
4. Sync: POST /api/calendars/sync (session path).
5. Read events via Directus admin or a smoke-only `GET /api/calendars/events?from=...&to=...` (optional helper).
6. Assert: 4 events present; declined event has `included_as_context = false`; all-day event has `included_as_context = true`; recurring event has `included_as_context = true`.
7. Exclude recurring (series): PATCH /api/calendars/events/[recurring-id] with `{ included_as_context: false }`. Re-read: all sibling occurrences also excluded; series_exclusions row exists.
8. Re-sync (manual): POST /api/calendars/sync. Assert: re-pulled events for the recurrence still default to excluded (series rule durable across syncs).
9. Re-include series: POST /api/calendars/events/[recurring-id]/include-series. Re-read: all siblings included; series_exclusions row gone.
10. Disconnect: POST /api/calendars/[id]/disconnect. Assert: connection gone, events gone, series_exclusions gone, Google grant revoked (manual check at https://myaccount.google.com/permissions).

**Total: ~119 enumerated tests** across 13 test files + 1 smoke. Tag-merge step-1 had 63 tests; calendar-binding step-1 has roughly double, justified by the OAuth surface + the multi-route fan-out.

---

## Done criteria

- [ ] Every AC above is GREEN
- [ ] RED was captured before implementation
- [ ] GREEN was captured after implementation
- [ ] Full suite still passes (no regressions on the ~1233 existing tests + step-0's ~40 new tests)
- [ ] `npm run typecheck` clean
- [ ] `npm run lint` clean
- [ ] `npm run verify` clean (lint + typecheck + Vitest)
- [ ] Production smoke 10/10 GREEN
- [ ] `verify-schema.mjs` GREEN against production
- [ ] `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET` Fly secrets confirmed set (names only; never values)
- [ ] Brainfog walkthrough: connect → choose → sync → exclude series → re-include passes on iPhone PWA without second-tap retries
- [ ] No new HIGH gate findings
- [ ] Refactor pass complete (or "none needed")

---

## Execution order

### 1.0 Setup (manual, before tests)

**Google Cloud Console:**

1. Create or select a Google Cloud project (one is fine: `gevoelscore-personal`).
2. Enable the Google Calendar API.
3. Configure OAuth consent screen: External, scopes = `calendar.readonly` only, test users = the developer's Google account.
4. Create OAuth 2.0 Client ID for "Web application". Authorized redirect URIs:
   - `https://gevoelscore-frontend.fly.dev/api/calendars/google/callback`
   - `http://localhost:3000/api/calendars/google/callback`
5. Copy Client ID + Client Secret.

**Fly secrets:**

```powershell
fly secrets set GOOGLE_CLIENT_ID=<from-google-console> -a gevoelscore-frontend
fly secrets set GOOGLE_CLIENT_SECRET=<from-google-console> -a gevoelscore-frontend
# CALENDAR_KEK is from step-0
# CALENDAR_SYNC_SECRET is from step-2 (set in step-2, not here)
```

**Local .env.local** (not committed; for `npm test` + local dev):

- `GOOGLE_CLIENT_ID=<same>`
- `GOOGLE_CLIENT_SECRET=<same>`
- `CALENDAR_KEK=<same as Fly>`

### 1.1 Baseline

Step-0 verifier `~70/70 OK`. Full test suite GREEN. Calendars collection empty (only the migrated schema from step-0).

### 1.2 Write tests (RED)

For each of the 13 test files enumerated above, paste the test code and stub the implementations with `throw new Error('not implemented')`. Run targeted tests, confirm failures.

### 1.3 Implement (GREEN)

Order within step-1:

1. `src/lib/integrations/google/google-provider.ts` (AC1.1-1.12)
2. `src/lib/sync/calendar-sync.ts` (AC1.13-1.23)
3. Routes in order: connect, callback, choose, sync, disconnect, per-event PATCH, include-series (AC1.24-1.52)
4. Components: CalendarsSection, ChooseCalendarsForm, CalendarEventSheet, ContextEventsSection (AC1.53-1.72)

Run `npm test -- calendar` after each unit; full `npm test` at the end.

### 1.4 Apply / deploy to production

```powershell
fly deploy -a gevoelscore-frontend
```

After deploy:

```powershell
# Run the production smoke (manual OAuth step inside)
.\scripts\run-calendar-binding-smoke.ps1
```

### 1.5 Refactor

Common refactors at this size:

- Hoist the route auth-stack into a helper (`withSessionOrBearer`, etc.) if duplication is heavy across the 6 routes
- Consolidate the per-event update logic into a single `applyEventUpdate(updates, event, connection)` function reused by PATCH + include-series
- Move the Dutch copy strings into `src/copy.ts` under a `calendarBinding` key (matches existing convention)

### 1.6 Walkthrough

This step touches the Context tab + adds a Settings surface. Walkthroughs:

1. **Sub-10s daily flow regression**: open app → tap score → close. Time must stay ≤ 10s. The Today card may show events (step-2) but step-1 doesn't change the Today card.
2. **Brainfog walkthrough of the Kalenders connect flow**: one-handed, low-light. Verbind → Google consent → return → kies kalenders → submit. Any second-attempt tap is a fail.
3. **Brainfog walkthrough of the Sluit-uit-series flow**: open Context for a day with a recurring event → tap event → tap Sluit uit. Must take exactly one tap and the row must disappear immediately. Then verify `Toon overgeslagen` reveals it greyed and `[Voeg hele serie weer toe]` restores it.
4. **Network-loss check**: DevTools Offline. Open Context → events render from local DB. Tap event → sheet opens. Tap Sluit uit → toast `Geen netwerk. Probeer opnieuw.` Reconnect → retry → success.

### 1.7 Checkpoint

Commit message:

```
calendar-binding/step-1: Google OAuth + Settings + manual sync + Context

OAuth provider (Google), three OAuth routes (connect/callback/disconnect),
sync route (session-gated; bearer path tested but cron lands in step-2),
sync orchestrator with 3 smart-default rules (all-day include, recurring
include, declined exclude). Settings surface with connect/refresh/ontkoppel.
Context tab events section + per-event detail sheet with tag/episode linking
and single-tap Sluit-uit (per-row default, series-default for recurring).
Asymmetric re-include: per-row by default, explicit [Voeg hele serie weer toe]
for series-level.

Refresh tokens encrypted at rest via the v1 envelope-encryption helper from
step-0. OAuth state cookie signed, SameSite=Lax, 10-minute Max-Age. No event
content in logs. Standard auth-stack pattern from merge-route mirrored across
all 6 new routes.

Acceptance criteria addressed: AC1.1 through AC1.78 (78/78).

Tests: ~119 new tests across 13 test files. Full suite GREEN. Production
smoke 10/10 against gevoelscore-frontend.fly.dev (manual OAuth step in
the middle of the run).
```

---

## Done (filled in during `/build-step`)

- [ ] AC1.1-1.78: per test file mapping above
- [ ] RED captured: `npm test -- calendar` → `~119 failing (not implemented)` on YYYY-MM-DD
- [ ] GREEN captured: `npm test -- calendar` → `~119 passing` on YYYY-MM-DD
- [ ] Type check clean
- [ ] Lint clean
- [ ] Verify gate clean
- [ ] Production smoke: 10/10 GREEN on YYYY-MM-DD
- [ ] `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET` Fly secrets set
- [ ] Daily-flow regression walkthrough: ≤10s on iPhone PWA
- [ ] Brainfog walkthrough Sluit-uit-series: single-tap, no second attempt
- [ ] Network-loss walkthrough: graceful error + retry
- [ ] No new HIGH gate findings
- [ ] Refactor: ...

---

## What this step does NOT do

- **No daily cron.** No GHA workflow, no automated daily sync. Only the manual `Ververs nu` path is wired. Cron lands in step-2.
- **No `/api/health/cron` endpoint.** Lands in step-2.
- **No Today card events region.** Lands in step-2.
- **No timeline overlay.** Lands in step-3.
- **No keyword exclusion rules.** Defer to v1.6.x.
- **No calendar-bound episodes (Shape B).** Defer to v1.6.1.
- **No learned-rules suggestion engine.** Defer to v2.
- **No Outlook / Apple provider.** Defer to v2.
- **No historical backfill UI.** The 7-back / 30-forward window is what we ship. If the user wants more, they extend the window via Directus admin (out-of-scope manual op).
- **No event-detail-screen as a route** (separate page). Per-event interaction stays inside a BottomSheet for thumb-first consistency.
- **No "save your changes" prompt** in the event sheet. Auto-save per change, matches the daily-flow contract.
- **No batch select-mode** for events. Per-event interaction only. Multi-select event ops are a v2 candidate if soak shows demand.
