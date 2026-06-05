# Calendar binding

**Feature:** Connect external calendars (Google first, design extensible to Outlook / Apple) so that events surface as **context** alongside the daily score. The user sees how the score fluctuates in the context of events and interventies. NOT a calendar app — context only.
**Version:** v1.6 (Shape A only — event-side linking; episode-side binding deferred to v1.6.1; see [Future considerations](#future-considerations))
**Status:** Steps 0-2 shipped (2026-06-05). Step 3 (timeline overlay) next; steps 4-6 deferred to v2 / v1.6.1 per [Future considerations](#future-considerations).
**Parent docs:** [REQUIREMENTS.md](../../REQUIREMENTS.md) (line 114 — `calendar_events` placeholder collection; line 124 — `src/lib/integrations/` interface; line 132 — `calendar.readonly` only) · [app_brief_gevoelscore.md](../../app_brief_gevoelscore.md) (Google Calendar sync v1.5+) · [technisch_document.md](../../technisch_document.md) (passive context, OAuth scopes) · [ADR 0002](../../decisions/0002-pwa-with-directus-backend.md) (online-first, self-hosted Directus)

---

## Overview

- **What:** OAuth-connect a Google Calendar account; pull events daily (plus on-demand "Ververs nu"); show them as **context** under the date they occur. Each event can optionally be linked to a tag (interventie / activiteit / project / gebeurtenis) or an episode, and can be excluded from context (single-tap, series-default).
- **Why:** A 1.363-day chronic-logging history shows score fluctuations whose causes are often calendar events (fysiotherapie afspraak, ziekenhuisbezoek, sociale belasting, werkmeeting, vakantie). Reading those into the app via OAuth removes the friction of dual-logging and surfaces the context that was previously only in the user's head.
- **Impact:** Settings gains a Kalenders surface. The Context tab on each day gains an event list. The Today card surfaces today's events. The Timeline gains subtle markers above the score line. The score-only daily flow is **unaffected** (cardinal-principle-protected).

---

## User need

> "Ik wil zien hoe mijn gevoelscore fluctueert in de context van wat er gebeurt — een afspraak, een drukke werkdag, een vakantie. Niet alle agenda-items zijn relevant; sommige zijn ruis (werkstandups, lunch-blocks). Ik wil eenmalig zeggen welke kalenders en welke events meedoen, en daarna wil ik er niet meer aan denken."

The brief and ADR 0002 both reserve calendar sync for a post-v1 version. The roadmap puts it at v1.6 — graduating now after the v1.5 anchor (verloop-and-episodes), v1.5a-d cleanup pack, and the daily-entry + popout features have settled.

---

## Acceptance criteria

Concrete, testable behaviors. Each line maps to one or more `it` blocks in the step file test plans.

### Connect / disconnect

- [ ] **AC1** Settings → Kalenders surface lists connected calendars with `provider_account_email + verbonden + laatst gesynchroniseerd Xu geleden`, `[Ververs nu]`, `[Ontkoppel]`. Empty state shows `+ Verbind een andere kalender` with Google enabled and Outlook / Apple greyed (`binnenkort`).
- [ ] **AC2** Tapping `Verbind Google Calendar` redirects to Google OAuth consent (full-page, not popup) with scope `https://www.googleapis.com/auth/calendar.readonly` only. State preserved via signed cookie.
- [ ] **AC3** Google consent callback exchanges the auth code for a refresh + access token, encrypts the refresh token at rest in `calendar_connections.refresh_token_encrypted` via envelope encryption (Fly secret as KEK).
- [ ] **AC4** After callback, the user lands on a `Kies kalenders` screen that lists the user's Google calendars (via the calendar list API). All are checked by default; the user can uncheck before submitting. Submission persists per-calendar inclusion to `calendar_connections.included_calendar_ids`.
- [ ] **AC5** Connecting the same Google account twice is idempotent (UNIQUE on `(user_id, provider, provider_account_email)`) — second connect updates included_calendar_ids, never creates a duplicate row.
- [ ] **AC6** `Ontkoppel` revokes the OAuth grant via Google's `/o/oauth2/revoke` endpoint, then deletes the `calendar_connections` row, then cascades to `calendar_events` + `calendar_series_exclusions`. Atomic best-effort: revoke first (so even if cascade fails, Google no longer has the grant).
- [ ] **AC7** `Ververs nu` triggers an immediate sync of the connected calendars from `last_synced_at` to now. Button shows `Synchroniseren...` while in flight; updates `last_synced_at` on completion.

### Sync logic

- [ ] **AC8** A single `POST /api/calendars/sync` route handles both manual (session-gated) and automated (bearer-gated via `CALENDAR_SYNC_SECRET`) triggers. Same code path, two auth gates. Auth-gate selection: if `Authorization: Bearer X` is present and matches the secret, treat as automated; else fall back to session auth.
- [ ] **AC9** Sync iterates active connections, refreshes the access token via the refresh token (Google `/oauth2/token` with `grant_type=refresh_token`), fetches events in a rolling window (default: 7 days back, 30 days forward — bounded to limit Google API quota usage and to keep the Today / Context surfaces fresh without dragging all-time history).
- [ ] **AC10** Events from un-included calendars (those the user unchecked at connect time) are NEVER fetched. Layer 1 filter is at the source.
- [ ] **AC11** Each fetched event is upserted into `calendar_events` by `UNIQUE(connection_id, provider_event_id)`. Stable events don't re-run downstream computation; changed events update title / time / attendees / declined-status / etc.
- [ ] **AC12** At pull time, each new event gets `included_as_context` computed from three smart-default rules:
  - All-day event → `true`
  - Recurring event → `true` (badge shown in UI to make exclusion easier)
  - Declined RSVP → `false`
  - No keyword stoplist. Default if none of the above triggers exclusion → `true`.
- [ ] **AC13** If a fetched event's `recurrence_id` matches a row in `calendar_series_exclusions`, that event's `included_as_context` defaults to `false` and `user_decision` is set to `'user_excluded'` so the series rule keeps applying to future occurrences.
- [ ] **AC14** A `user_decision` field on `calendar_events` records `'auto' | 'user_included' | 'user_excluded'`. Set to `'auto'` for new events; flips to user-decision values when the user toggles include/exclude. Captures signal for v2 learned rules at no extra cost in v1.6.
- [ ] **AC15** Sync writes one row in `cron_monitor` for `daily_calendar_sync` with `last_run_at`, `last_result` (e.g. `{ connections: 1, events_pulled: 12, events_upserted: 3 }`). Errors are also written (`last_result` carries the error code; HTTP-500-style failures don't prevent the row update).

### Context tab per-day

- [ ] **AC16** The Context tab on each day renders a section `Activiteiten` listing all `calendar_events` with `included_as_context = true` that overlap that date (start_at..end_at overlaps the day in the user's local timezone). Events sorted by `start_at` ascending; all-day events first.
- [ ] **AC17** Each event row shows: time (or `Hele dag`), title, optional location, optional linked-tag badge `→ <tag.label>`, optional linked-episode badge `→ <episode.label>`. Recurring events show a small recurrence icon.
- [ ] **AC18** Tapping an event row opens a nested BottomSheet (per `[[design_principle_thumb_first_input]]`) with the event detail: title, full datetime, location, linked-tag picker, linked-episode picker, `[Sluit uit als context]` button. Closes on drag-down / Escape / outside-tap. No "save" button — auto-save per change, mirroring the daily-flow contract.
- [ ] **AC19** Linking a tag from the event sheet updates `calendar_events.linked_tag_id` and refreshes the per-event row. Only non-archived tags shown; categories `interventie / activiteit / project / gebeurtenis` highlighted at the top.
- [ ] **AC20** Linking an episode from the event sheet updates `calendar_events.linked_episode_id`. Lists non-archived episodes sorted by start_date desc.
- [ ] **AC21** `Sluit uit als context` on a non-recurring event sets `included_as_context = false` + `user_decision = 'user_excluded'` and removes the row from the Context tab. Single tap, no modal.
- [ ] **AC22** `Sluit uit als context` on a recurring event inserts a row into `calendar_series_exclusions(connection_id, recurrence_id)` AND sets all sibling events with that `recurrence_id` to `included_as_context = false` + `user_decision = 'user_excluded'` via one bulk PATCH. Single tap, no modal. **Default exclusion is series-level** ("this is not a calendar app, it's context" — coarse decision).
- [ ] **AC23** A `Toon overgeslagen events` toggle on the Context tab surfaces excluded events with reduced opacity. From here, a per-row `Weer meenemen` action sets `included_as_context = true` + `user_decision = 'user_included'` for that one event only (asymmetric: re-include is per-row, not series). The series rule still applies to OTHER occurrences.
- [ ] **AC24** Inside the event detail sheet for an excluded recurring event, a `Voeg hele serie weer toe` button DELETEs the matching `calendar_series_exclusions` row AND bulk-PATCHes all sibling events to `included_as_context = true` + `user_decision = 'user_included'`.

### Today card

- [ ] **AC25** The Today card gains a small `Vandaag` events region listing today's `included_as_context = true` events with time + title. Tap an event row to open the same per-event sheet as AC18. Region collapses to count if there are more than 3 events (`+ N meer`).

### Timeline

- [ ] **AC26** The timeline renders subtle markers above the score line for days that have any `included_as_context = true` event. Marker style: thin warm-earth tick (existing design token), not warm-orange / alarm. Tap a marker → opens the Context tab for that date.
- [ ] **AC27** Multi-day events (start_at and end_at span more than one calendar day in the user's timezone) render as a faint horizontal bar spanning the affected days, layered behind the score line. One canonical event in DB, derived rendering across days.

### Cron / health

- [ ] **AC28** A GitHub Actions workflow `daily-calendar-sync.yml` triggers `POST /api/calendars/sync` with `Authorization: Bearer ${{ secrets.CALENDAR_SYNC_SECRET }}` every day at `0 3 * * *` UTC.
- [ ] **AC29** A new `cron_monitor` Directus collection (schema matches programmeerprobeer's: `job_name UNIQUE`, `last_run_at`, `last_result`, `expected_interval_hours`, `is_active`) has one seeded row: `('daily_calendar_sync', NULL, NULL, 26, true)`.
- [ ] **AC30** `GET /api/health/cron` reads `cron_monitor`, computes per-job staleness against `expected_interval_hours`, returns JSON `{ status, jobs[] }`. Same shape as programmeerprobeer's endpoint.
- [ ] **AC31** A second GitHub Actions workflow `cron-health-check.yml` polls `/api/health/cron` every 6 hours. Workflow fails (auto-emails maintainer) if any job is `stale` or `never_run`.

### Privacy / export / delete

- [ ] **AC32** No event title, location, or attendee data is logged anywhere (server logs, cron_monitor.last_result, error responses). Counts and `provider_event_id` only.
- [ ] **AC33** CSV / JSON export includes `calendar_events` (all fields) and `calendar_connections` (everything except `refresh_token_encrypted`).
- [ ] **AC34** Full delete via Directus admin removes `calendar_connections` + `calendar_events` + `calendar_series_exclusions`. No orphan rows.

---

## Technical constraints

### Privacy / security (load-bearing — calendar refresh tokens are the highest-value secret in the app)

- **Encrypted at rest.** `calendar_connections.refresh_token_encrypted` is AES-GCM-encrypted at the app layer with a Fly secret as the KEK. The Directus admin role can read the column (for export / debugging) but the scoped frontend role MUST NOT have read on this column.
- **No event content in logs.** Server logs, cron_monitor.last_result, and error responses contain counts + provider_event_ids ONLY. Never titles, locations, attendees.
- **OAuth scope is narrowest.** `https://www.googleapis.com/auth/calendar.readonly` — no write scope, no other Google product scopes, no `userinfo` beyond what's needed for the connection email.
- **Fly secrets only.** `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET` + `CALENDAR_SYNC_SECRET` + `CALENDAR_KEK` are Fly secrets. The first three are also GitHub Actions secrets where needed. **None** are `NEXT_PUBLIC_*`.
- **CSRF posture.** OAuth state cookie is signed; callback validates the cookie against the returned `state` parameter. Sync route under standard origin / session / rate-limit gates per [src/app/api/tags/[id]/merge/route.ts](../../../src/app/api/tags/[id]/merge/route.ts).
- **Full-delete revokes Google grant.** Disconnect / full-delete calls Google's `/o/oauth2/revoke` endpoint with the refresh token to remove the grant on Google's side, then deletes the local row. Best-effort: if the revoke call fails (e.g. token already revoked), the local cascade still runs.
- **Export includes events; refresh token excluded.** The export of `calendar_connections` strips `refresh_token_encrypted` (it's a secret of a different shape than the user's data — they can re-connect to get a new one, but we never include it in a portable export).

### Storage / schema

- **Migration of the existing `calendar_events` placeholder.** The v1 placeholder (created in [directus/scripts/setup-schema.mjs:427-510](../../../directus/scripts/setup-schema.mjs#L427)) is Google-specific (`google_event_id` UNIQUE, `calendar_source`, `relevance` enum, `category_hint`). Empty in production. Step-0 migrates the schema to the multi-provider shape (`provider`, `provider_event_id`) so the v1 reservation isn't a Google-only lock-in. Migration is non-destructive (collection is empty); the script asserts `SELECT COUNT(*) = 0` before dropping columns.
- **Three new collections** plus the one migration:
  - `calendar_events` (migrated)
  - `calendar_connections` (new)
  - `calendar_series_exclusions` (new)
  - `cron_monitor` (new — shared infrastructure, will outlive this feature)
- **`episodes.calendar_binding` stays locked to null in v1.6.** Step-0 updates the stale "v1.6" comment in [src/lib/api/episodes.ts](../../../src/lib/api/episodes.ts) and [src/lib/domain/episode.ts](../../../src/lib/domain/episode.ts) to point at **v1.6.1** instead (the calendar-bound-episodes feature). See [Future considerations](#future-considerations).
- **UNIQUE / INDEX additions** (in the SQL migration):
  - `UNIQUE(connection_id, provider_event_id)` on `calendar_events` for idempotent upsert.
  - `UNIQUE(user_id, provider, provider_account_email)` on `calendar_connections` for idempotent connect.
  - `UNIQUE(connection_id, recurrence_id)` on `calendar_series_exclusions`.
  - `UNIQUE(job_name)` on `cron_monitor`.
  - Index on `calendar_events(connection_id, start_at)` for date-range queries on the Context tab.
  - Index on `calendar_events(connection_id, recurrence_id)` for series operations.

### Performance / quota

- **Daily sync window: 7 days back, 30 days forward.** Bounded against Google's per-user quota (default 1M queries/day, easy to stay under for a single user) and the size of the Context surfaces. Bounded re-pull on each sync recomputes status for events near today; old events stay frozen.
- **Manual `Ververs nu` uses the same bounded window.** Not "pull everything since connect" — that would be O(connect_age) every tap. If the user wants to backfill further (e.g. linked a tag to an event from 6 months ago), they can use the existing date-range UI in Directus admin to extend the window for a one-off pull (out-of-scope for v1.6 UI).
- **Bulk SDK operations.** Bulk PATCH / DELETE for series-level exclusion (one `updateItems` over the recurrence_id sibling set, same pattern as [src/lib/api/tags.ts mergeTag](../../../src/lib/api/tags.ts) bulk operations from v1.5c).

### Online-first per ADR 0002

- Sync requires network. Offline degradation is "show last-synced events" — the Context / Today / Timeline render against the local Directus copy, which is already-pulled. No write happens offline; the `Sluit uit` toggle requires network (matches the online-first daily flow per ADR 0002).
- `Ververs nu` shows a clear error toast on network failure with `[Probeer opnieuw]`. Matches the [day-entry online-failure pattern](../../../src/components/quick-entry-flow.tsx).

### Cron infrastructure (NEW for this project)

- **This is the first scheduled job in gevoelscore-app.** The `cron_monitor` collection + `/api/health/cron` endpoint + watchdog GHA workflow establish the convention. Future jobs (export, retention sweeps, learned-rules aggregation) reuse the same infrastructure.
- **Execution path = GitHub Actions cron → Next.js endpoint** (not a Directus Flow). Reasons:
  - OAuth secrets already live in Fly env (no Flow context duplication)
  - Sync logic belongs in the Next.js codebase (testable, deployable, code-review surface)
  - Sibling project ([programmeerprobeer](c:\Users\Gebruiker\Documents\programmeerprobeer)) has a [documented Flow-rebuild migration](c:\Users\Gebruiker\Documents\programmeerprobeer\directus\scripts\migrations\rebuild-flows-for-11.17.js) after a Directus upgrade — fragility on a load-bearing job is unacceptable.
- See [step-2-daily-cron-and-today.md](./step-2-daily-cron-and-today.md) for the full cron-infrastructure breakdown.

---

## Test plan

Layer-by-layer test file map. Test code is named (not pasted) here; the step files paste the actual code per the [TDD doctrine](../../../.claude/testing.md).

| Layer | File | Step | Cases (one per `it`) |
|---|---|---|---|
| Domain (event types, smart-default rules) | `src/lib/domain/__tests__/calendar-event.test.ts` | 0, 1 | All-day → include; Recurring → include; Declined RSVP → exclude; default → include; existing series exclusion overrides defaults |
| Domain (CalendarProvider interface contract) | `src/lib/domain/__tests__/calendar-provider.test.ts` | 0 | Interface shape; canonical CalendarEvent shape stable |
| Encryption helper | `src/lib/auth/__tests__/envelope-encryption.test.ts` | 0 | Encrypt → decrypt round-trip; tampered ciphertext fails; wrong KEK fails; nonce included; key rotation supported (out of scope for build, but interface allows it) |
| Google provider | `src/lib/integrations/google/__tests__/google-provider.test.ts` | 1 | Token refresh; calendar list fetch; events fetch with timeMin / timeMax; recurrence_id captured; declined-attendee detection; pagination handling |
| Sync orchestrator | `src/lib/sync/__tests__/calendar-sync.test.ts` | 1, 2 | Bounded window; per-connection iteration; upsert idempotent on re-run; series-exclusion rule applied on insert; user_decision = 'auto' on new; cron_monitor write on success + on error |
| API: connect | `src/app/api/calendars/google/connect/__tests__/route.test.ts` | 1 | Origin / session gate; redirect URL well-formed; state cookie set |
| API: callback | `src/app/api/calendars/google/callback/__tests__/route.test.ts` | 1 | State cookie validation; code exchange; row insert; calendars listed; redirect to Settings |
| API: choose-calendars | `src/app/api/calendars/[connection_id]/calendars/__tests__/route.test.ts` | 1 | Origin / session / ownership gates; included_calendar_ids persisted |
| API: disconnect | `src/app/api/calendars/[connection_id]/disconnect/__tests__/route.test.ts` | 1 | Revoke called; cascade delete; revoke failure still cascades |
| API: sync | `src/app/api/calendars/sync/__tests__/route.test.ts` | 1, 2 | Session-gated path 200; bearer-gated path 200; both gates fail → 401; rate-limit; sync orchestrator called once per connection |
| API: per-event-update | `src/app/api/calendars/events/[id]/__tests__/route.test.ts` | 1 | Origin / session gate; linked_tag_id update; linked_episode_id update; included_as_context toggle (non-recurring); series exclusion (recurring) |
| API: series-include | `src/app/api/calendars/events/[id]/include-series/__tests__/route.test.ts` | 1 | Series exclusion row DELETED + bulk PATCH all siblings included |
| API: health | `src/app/api/health/cron/__tests__/route.test.ts` | 2 | OK when all jobs fresh; warning when never_run; stale when over threshold; error when collection unreachable |
| Component: Settings → Kalenders | `src/components/__tests__/calendars-section.test.tsx` | 1 | Empty state; connected state; Verbind button initiates OAuth flow; Ververs nu shows in-flight state; Ontkoppel triggers confirm |
| Component: choose-calendars screen | `src/components/__tests__/choose-calendars-form.test.tsx` | 1 | All checked by default; uncheck persists; submit returns to Settings |
| Component: per-event detail sheet | `src/components/__tests__/calendar-event-sheet.test.tsx` | 1 | Tag link; episode link; sluit-uit non-recurring; sluit-uit recurring (series); voeg hele serie weer toe; sluit-uit closes sheet + refreshes |
| Component: Context tab events | `src/components/__tests__/context-events-section.test.tsx` | 1 | Renders events overlapping date; sorts by time; all-day first; recurrence badge; Toon overgeslagen toggle |
| Component: Today card events | `src/components/__tests__/today-events-region.test.tsx` | 2 | Today's events; collapse-to-count over 3; tap opens sheet |
| Component: Timeline overlay | `src/components/__tests__/timeline-event-markers.test.tsx` | 3 | Tick on event days; multi-day spans render as bar; warm-earth color (not alarm) |
| Smoke (prod): connect → sync → exclude → reconnect | `scripts/calendar-binding-smoke.mjs` | 1, 2 | Real OAuth flow; real Google events fetched; series exclusion persists across re-sync; disconnect revokes + cascades |
| Smoke (prod): cron round-trip | `scripts/calendar-cron-smoke.mjs` | 2 | GHA fires; sync route returns 200; cron_monitor row written; health endpoint reports fresh |

Total: **~80 enumerated test cases** across 18 files, plus 2 production smokes. Step files contain the paste-ready code.

---

## Cardinal-principle impact

| Principle | Impact | How we stay inside |
|-----------|--------|--------------------|
| One-tap entry | None on daily flow | Calendar binding adds context surfaces (Settings to set up, Context / Today / Timeline to view). The score-only flow remains: tap score → done. No new tap in the path. |
| Sub-10-second flow | None on daily flow | Today's events region is read-only on the Today card; it adds nothing to the entry path. Event-linking is a Context-tab activity, not a daily-entry activity. |
| Brainfog-friendly | Lowest-friction series exclusion possible | Series-default exclusion (one tap, no modal). Layer 1 calendar-level filter at connect time keeps per-event decisions sparse. Picker / sheet pattern matches existing surfaces (tag picker, episode picker) so the user re-uses muscle memory. |
| No unsolicited notifications / ads / analytics | None added | No Google Analytics, no metrics SDK, no notification API used. The OAuth-revoke + full-delete paths ensure the user remains in control. |
| User-owned data | Calendar events become part of the user's data corpus | Events live in self-hosted Directus. Export includes them. Full-delete removes them + revokes the Google grant. **Refresh tokens are excluded from export** (they're an access secret, not user data; user re-connects to get a new one). |
| Export / delete still works | New collections covered | `calendar_events` (full) + `calendar_connections` (minus refresh_token_encrypted) + `calendar_series_exclusions` join the export. Full-delete cascades all three collections + calls Google's revoke endpoint. |

No HIGH findings. All cardinal-principle gates pass.

---

## Alternatives considered

### Decision 1: Provider abstraction or Google-only

- **Chose:** Provider abstraction (`CalendarProvider` interface + canonical `CalendarEvent` shape) with Google as the only v1.6 implementation.
- **Considered and rejected:** Google-only with `google_event_id` / `google_calendar_id` columns directly on `calendar_events`. The placeholder schema already does this. Rejected because the user explicitly wants Outlook / Apple to be plausible v2 extensions, and a multi-provider migration after data exists is far costlier than the migration we do in step-0 (the collection is empty).
- **Revisit when:** Never expect to. The interface is small (3 methods); abstraction cost is one extra file.
- **Migration path:** N/A — chose the abstraction up front.

### Decision 2: GitHub Actions cron vs Directus Flow vs Fly Machines scheduled

- **Chose:** GitHub Actions cron → Next.js endpoint, with `cron_monitor` + watchdog GHA. Same pattern as [programmeerprobeer](c:\Users\Gebruiker\Documents\programmeerprobeer).
- **Considered and rejected:** Directus Flow with a JS exec operation. Rejected because (1) OAuth secrets duplicate awkwardly into the Flow context, (2) the sibling project documents Flow-rebuild migrations across Directus upgrades, (3) sync logic belongs in the same codebase as the OAuth + rendering code.
- **Considered and rejected:** Fly Machines `[processes]` cron worker. Rejected because Fly's scheduled-machine UX is less observable than GitHub Actions logs, and we'd be adding infra knowledge load for marginal benefit.
- **Considered and rejected:** Vercel cron. N/A — the app is on Fly, not Vercel.
- **Revisit when:** If GitHub Actions becomes unreliable for our use case (e.g. consistently late firings). The migration to a Directus Flow would be the next-cheapest fallback.
- **Migration path:** The route is the same in any execution model; only the trigger changes. Moving the schedule to a Directus Flow would be ~50 lines of JS exec wrapped around the existing `POST /api/calendars/sync` HTTP call.

### Decision 3: OAuth popup vs full-page redirect

- **Chose:** Full-page redirect.
- **Considered and rejected:** Popup with `window.postMessage` back to the opener. Rejected because (1) popups are blocked aggressively in iOS Safari (the daily-driver context), (2) postMessage state recovery is brainfog-hostile if it fails, (3) full-page redirect is the standard pattern for installed PWAs.
- **Revisit when:** Never expect to.
- **Migration path:** N/A.

### Decision 4: Pull cadence — daily vs monthly

- **Chose:** Daily background pull + on-demand `Ververs nu`.
- **Considered and rejected:** Monthly. The user's first instinct. Rejected because (1) Today card integration requires < 1 day staleness, (2) Google API quota is generous enough that daily is free, (3) monthly leaves a 29-day "today" blind spot.
- **Revisit when:** If Google starts rate-limiting on this app's quota, drop to weekly + manual ververs. Unlikely for single-user usage.
- **Migration path:** Change the `cron:` line in `daily-calendar-sync.yml`.

### Decision 5: Smart-default include/exclude rules

- **Chose:** Three rules: all-day → include, recurring → include with badge, declined RSVP → exclude. No keyword stoplist.
- **Considered and rejected:** Keyword stoplist (`Standup`, `Lunch`, `Block`, `Focus time`). Rejected because (1) `Block` and `Focus time` ARE work blocks per the user principle "people use these as reminders or blocks to do work as part of planning", (2) keyword lists are paternalistic — they encode my guesses about what's noise.
- **Considered and rejected:** Zero-duration / 0-attendee → exclude. Rejected per user correction 2026-06-03 (same reason as the stoplist).
- **Revisit when:** v1.6.1+ — let the user define their own keyword rules from real exclusion patterns. The `user_decision` field captures the signal.
- **Migration path:** A new `calendar_keyword_rules` collection plus matching logic at pull time. Logic touchpoint = `src/lib/sync/calendar-sync.ts` (single function).

### Decision 6: Series exclusion shape — coarse-default vs per-occurrence

- **Chose:** Series-level by default. Single tap on `Sluit uit als context` excludes the whole series (past + future). Re-include is per-row (asymmetric).
- **Considered and rejected:** Per-occurrence default with `Ook toekomstige` toggle. Rejected because the asymmetric "coarse exclude, fine re-include" matches the user mental model better: "I never want this as context" is coarse, "this one specific instance was meaningful" is fine.
- **Considered and rejected:** Modal asking "deze of alle?". Brainfog-hostile.
- **Revisit when:** v1.6.1+ if soak shows excluded-series users frequently re-including past instances. Inline "alleen deze keer" link in the event sheet is the smallest possible fallback.
- **Migration path:** Add a `[Sluit alleen deze keer uit]` underlined link below the primary button in the event detail sheet.

### Decision 7: Episode binding — Shape A (event-side link) vs Shape B (episode-side binding)

- **Chose:** Shape A only in v1.6. `calendar_events.linked_episode_id` carries the link. `episodes.calendar_binding` stays locked to null with its existing validator gate; the column comment is updated in step-0 to point at v1.6.1.
- **Considered and rejected:** Shape B in v1.6. Rejected because it opens design questions (exclude-while-bound, recurrence cancellation, manual vs auto promotion) that weren't in the four design conversations and would expand v1.6 scope significantly.
- **Considered and rejected:** Both shapes in v1.6. Same reason.
- **Revisit when:** After v1.6 soak. If the user is frequently linking many events to a single episode (every Tuesday yoga event → "Yoga met Anna" episode), that signals Shape B would remove the per-event linking burden. Graduate as v1.6.1.
- **Migration path:** Shape B is additive: define the `calendar_binding` shape (`{ provider, connection_id, recurrence_id } | null`), unlock the validator, add a "Maak episode van deze serie" action in the event sheet, render bound-episode lifecycle. No data migration needed (existing `linked_episode_id` continues to work for non-bound events).

---

## Future considerations

Things deliberately deferred. Each marked with trigger signals + proposed approach.

### v1.6.1 — Calendar-bound episodes (Shape B from Decision 7)

- **What:** "Promote" a recurring calendar series to an episode that auto-tracks it. `episodes.calendar_binding = { provider, connection_id, recurrence_id }` makes the episode lifecycle (start_date, end_date, ongoing) derive from the bound recurrence. Every occurrence is implicitly part of the episode.
- **Trigger signal:** Soak data shows the user frequently linking events to a single episode (≥ N events linked to the same episode over a period of weeks).
- **Proposed approach:** Step file `step-6-calendar-bound-episodes.md` (to be written when triggered). Adds: validator unlock, `Maak episode van deze serie` action in the event detail sheet, episode-form treatment for bound episodes (read-only date fields), bound-episode lifecycle on series cancellation.

### v1.6.x — User-defined keyword exclusion rules

- **What:** Settings → Kalenders → Regels. User adds rules like `title contains "Standup" → uitsluiten` or `attendee count > 8 → uitsluiten`. Applied at pull time.
- **Trigger signal:** Soak shows > 5 per-event exclusions per week with recognisable patterns (same recurrence excluded multiple times before a rule could be encoded).
- **Proposed approach:** New `calendar_keyword_rules` collection. Logic touchpoint = `src/lib/sync/calendar-sync.ts`. The `user_decision` field already in v1.6 makes a "suggest a rule based on excluded patterns" affordance trivial in v2.

### v2 — Learned suggestion rules

- **What:** When a new event arrives and N similar past events were excluded by the user, default to exclude. Surfaces a `Suggestie: deze series uitsluiten? (X eerder uitgesloten)` prompt.
- **Trigger signal:** v1.6 + v1.6.x soak data shows clear patterns in `user_decision` field.
- **Proposed approach:** Background aggregation script writes to a `calendar_pattern_decisions` collection; sync applies the rules at pull time. No new external dependency; all the signal is already captured.

### v2 — Second / third provider (Outlook, Apple)

- **What:** Connect a Microsoft 365 / Outlook.com or iCloud calendar. Same UX: connect → choose calendars → events flow through.
- **Trigger signal:** User asks for it. (Single user; no abstract demand to model.)
- **Proposed approach:** New `OutlookCalendarProvider` / `AppleCalendarProvider` implementations of the `CalendarProvider` interface. Provider-specific OAuth flow + event-fetching; the canonical `CalendarEvent` shape stays identical; downstream (sync orchestrator, smart-default rules, UI) is provider-agnostic.

### v2 — Historical backfill as an onboarding action ("Importeer geschiedenis")

- **What:** Productize the admin-only `scripts/calendar-historical-backfill.mjs` into a user-facing onboarding step on `/settings/kalenders/choose` (right after first OAuth + calendar selection). User picks a start date ("Hoe ver terug wil je je agenda meenemen?"), the server runs chunked syncs against the user's connection (re-uses the existing `/api/calendars/sync?from=&to=` window override), and a progress UI streams ("46 van 92 maanden verwerkt..."). When the backfill ships in v2 alongside multi-user, also wire it as the default action on a fresh OAuth connect so the Context tab feels populated from day one.
- **Why it matters:** Solves the new-user cold-start problem. The author's own 1788-event backfill (2022-09 → 2026-06) was the difference between a Context tab that looks "empty / broken" and one that immediately reflects months of patterns. For a Long COVID app where pattern discovery IS the value proposition, an empty Context tab on day one suppresses the very signal the user came for.
- **Trigger signal:** Multi-user rollout (the app starts being served to others). Until then the admin script is sufficient — the author backfills their own history once.
- **Proposed approach:**
  - New route `POST /api/calendars/[connection_id]/backfill` taking `{ from: 'YYYY-MM-DD' }`. Server-side chunks the range into 30-day windows (same logic as the script). Background-queue or streaming-response — likely the latter for v2 simplicity (Server-Sent Events with chunk-progress messages).
  - UI: a single date field + a primary `[Importeer]` button. Brainfog-friendly: no multi-step wizard, no "are you sure" — the action is reversible (re-running with a shorter range doesn't delete data, and `Ontkoppel` cascades).
  - Default start date: maybe 1 year back. Configurable. Cap at 5 years to keep Google API quota predictable.
  - Privacy: same as live sync — events flow only between Google and the user's own Directus.
  - Rate-limit / quota: piggyback the existing `calendarWriteRateLimiter` per-IP, plus a per-connection quota counter so a single user's backfill can't starve other users' live syncs.
- **Open questions:** Whether to surface the backfill action AGAIN later (e.g. "I started 6 months ago, now I want to import 2 more years"), or make it one-shot at connect. Soak with the first non-author users will answer that.

### Out of scope (won't ship)

- **Write back to calendar.** Read-only is a hard line. We are not a calendar app.
- **Calendar event creation from the app.** Users have a calendar app for that. We surface events, we don't author them.
- **Sharing / multi-user calendar views.** Single-user app per [REQUIREMENTS.md](../../REQUIREMENTS.md).
- **Push notifications on event start.** No unsolicited notifications per cardinal principle.

---

## Privacy & permissions

- **OAuth scopes requested:** `https://www.googleapis.com/auth/calendar.readonly` only. No `userinfo` beyond what comes for free with the OAuth flow (`email`, used only to populate `provider_account_email` for display).
- **Where the data lives:** All event data + connection metadata in the author's self-hosted Directus on Fly.io. Refresh tokens encrypted at rest. No third-party storage / sync.
- **Data that leaves the author's infrastructure:**
  - Outbound to `accounts.google.com` (OAuth consent + token refresh)
  - Outbound to `www.googleapis.com/calendar/v3/*` (event fetching)
  - Outbound to `oauth2.googleapis.com/revoke` (disconnect)
  - No other third-party calls. No analytics, no error tracking with PII.
- **Opt-in surface:** Settings → Kalenders → `[Verbind Google Calendar]`. Per-calendar inclusion is a second opt-in at connect time. The feature is OFF by default until the user actively connects.
- **Export coverage:** `calendar_events` (full), `calendar_connections` (minus `refresh_token_encrypted` — see security rationale), `calendar_series_exclusions` (full). Postgres dump via Directus admin always includes everything.
- **Delete coverage:**
  - `Ontkoppel` for one connection: revoke → cascade-delete events + series_exclusions + connection row.
  - Full-delete (e.g. via Directus admin "delete all my data" or future Account-deletion feature): cascade all three collections + best-effort revoke. The watchdog cron_monitor row stays (it's infra metadata, not user data).

---

## Security

Threat framing: **OWASP ASVS L2 + Top 10**, single-user, self-hosted Directus, OAuth integration. Refresh tokens are the highest-value secret in the app — they grant long-lived read access to the entire calendar.

### Access control (A01, A07)

- **Session gate on all routes** that touch user-scoped data. Pattern matches [src/app/api/tags/[id]/merge/route.ts](../../../src/app/api/tags/[id]/merge/route.ts): origin → session → rate-limit → UUID → body parse → lib call.
- **OAuth state cookie signed** with `SESSION_SECRET` (existing Fly secret). Callback validates the cookie against the returned `state` parameter; mismatch → 400.
- **Scoped Directus role for the frontend** cannot read `calendar_connections.refresh_token_encrypted`. Only the admin role + the sync-route service token can. The scoped role can still read all OTHER `calendar_connections` columns for display in Settings.
- **Bearer gate on the cron path** of `/api/calendars/sync` uses `CALENDAR_SYNC_SECRET` (Fly secret + GHA secret). Constant-time comparison.
- **Ownership check** on per-connection operations: `WHERE connection.user_id = session.user_id`. Defensive — only one user in v1.6 — but enforced for v2 multi-user readiness.

### In transit

- HTTPS-only for Directus (Fly-managed). HTTPS-only for Google OAuth + Calendar API (Google-managed). No mixed content.
- Manifest, redirect URIs, allowed origins all `https://gevoelscore-frontend.fly.dev` + `http://localhost:3000` (dev only).

### At rest

- **Refresh tokens AES-GCM encrypted** at the app layer. Envelope encryption: a random per-row DEK (Data Encryption Key) is generated, used to encrypt the refresh token, then the DEK itself is encrypted by the KEK (`CALENDAR_KEK` Fly secret) and stored alongside the ciphertext. This is the standard library pattern for "encrypt secrets in a managed DB" and supports key rotation (rotate KEK → re-encrypt all DEKs without re-encrypting the underlying secrets).
- **Postgres-at-rest encryption** via Fly defaults (LUKS).
- **Backups** are encrypted via Fly defaults.
- No source maps in production.

### Injection / untrusted input (A03)

- **Zod validation** at the route boundary for every body. Schemas in `src/lib/validation/calendar-binding.ts`.
- **Google API responses Zod-validated** before being trusted by the upsert. Google's API is documented but the responses go through the same boundary check as user input.
- **CSV export of events** uses the existing formula-injection-safe export helpers (`'`-prefix on cells starting with `=`, `+`, `-`, `@`).
- **No `dangerouslySetInnerHTML`** anywhere in the new components.

### Web surface

- **CSP allowlist** updated: `accounts.google.com` + `oauth2.googleapis.com` added to `connect-src` for the OAuth flow. No script-src additions (no third-party scripts loaded; OAuth is server-side).
- **Redirect URIs allowlist** at Google: exactly `https://gevoelscore-frontend.fly.dev/api/calendars/google/callback` + dev URI. Wildcards prohibited.
- **No user-controlled href / src / style** introduced. Event titles + locations are rendered as text only.

### Permissions (least privilege)

- OAuth scope is `calendar.readonly` only. No write, no other Google product scope (Drive, Gmail, Tasks).
- Browser permissions: none requested. The flow is server-side OAuth + Next.js routes; no `navigator.geolocation`, no `Notification.requestPermission`, no `Permissions` API.

### PWA-specific

- Service worker does NOT cache OAuth callback URLs (they contain one-time codes).
- Service worker does NOT cache `/api/calendars/google/connect` (returns a 302 with a fresh state cookie every call).
- `manifest.webmanifest` unchanged.

### Build hygiene & logging (A09)

- **No `console.log` of event titles, locations, attendees, or any OAuth payload.** Counts + provider_event_ids only.
- **Generic error responses.** Sync failures return `server_error` + an error code; never include the Google API error body or stack trace.
- **No telemetry deps added.** `npm audit` clean before merge.

### Supply chain

- `googleapis` (or `@google-cloud/local-auth` for the OAuth helper; TBD in step-1 between minimal-deps options) — official Google SDK, audited.
- No other new external dep planned. Encryption uses Node's built-in `crypto` (no `node-forge`, no `crypto-js`).

### OWASP ASVS sections explicitly walked

| Section | Coverage in this feature |
|---|---|
| V2 Auth | Session gate already established; OAuth state cookie signed; refresh token encrypted; revoke on disconnect |
| V3 Session | Existing `httpOnly`+`Secure`+`SameSite=Strict` cookies; bearer gate uses constant-time comparison |
| V4 Access Control | Per-connection ownership check; scoped role can't read refresh token; revoke chain on disconnect |
| V5 Validation | Zod schemas at route boundary + Google API response boundary; no `dangerouslySetInnerHTML` |
| V7 Error Handling | Generic error responses; no stack traces leak; no PII in logs |
| V8 Data Protection | Refresh tokens encrypted; export excludes refresh tokens; full-delete cascades + revokes |
| V11 Business Logic | Rate limit on sync route (per-user budget); idempotent upsert via UNIQUE constraints; series exclusion is bulk-atomic |
| V14 Configuration | All secrets are Fly secrets; no `NEXT_PUBLIC_*`; redirect URI allowlist tight |

---

## v1.5 / v2 readiness

- **Directus schema impact:** Three new collections + migration of one v1 placeholder (`calendar_events` Google-specific → multi-provider shape). Plus one shared-infra collection (`cron_monitor`) that outlives this feature. All migrations additive or no-data (placeholder is empty in production).
- **`DayEntry` impact:** Unchanged. `calendar_events` joins to days by date, not by FK. The nullable `garmin / health / weather / calendar_events / project_entries / derived` reservation rule from REQUIREMENTS line 114 is respected — `calendar_events` was the placeholder, now used; the others remain nullable for v2.
- **Other schema impact:**
  - `episodes.calendar_binding` column unchanged in v1.6 (still locked to null by validator). Comment updated to point at **v1.6.1**.
  - `tags` collection unchanged.
- **Integration shape:** Establishes `src/lib/integrations/{provider}/` directory (REQUIREMENTS line 124 — required to exist; this is the first one). Pattern: `connect()`, `fetchEvents(from, to)`, `disconnect()`. Future Outlook / Apple providers slot in alongside.
- **Cron infrastructure:** Establishes the `cron_monitor` collection + `/api/health/cron` + watchdog GHA pattern that will be reused for v2 jobs (export, retention sweeps, learned-rules aggregation, future episode reminders if they're ever enabled and remain opt-in per the cardinal principle).
- **Deferred assumptions:**
  - **v1.6.1 — Calendar-bound episodes** (`episodes.calendar_binding` shape). Trigger: real linking patterns from v1.6 soak.
  - **v1.6.x — Keyword exclusion rules.** Trigger: > 5 per-event exclusions/week with recognisable patterns.
  - **v2 — Learned suggestion rules.** Trigger: v1.6.x soak data.
  - **v2 — Outlook / Apple providers.** Trigger: user asks.

---

## Architecture

### File tree

```
docs/features/calendar-binding/
  README.md                       (this file)
  step-0-data-model-and-provider.md
  step-1-google-oauth-and-context.md
  step-2-daily-cron-and-today.md
  step-3-timeline-overlay.md
  step-4-v2-learned-rules.md      (defer marker)
  step-5-v2-second-provider.md    (defer marker)
  step-6-v1.6.1-calendar-bound-episodes.md  (defer marker)

src/lib/integrations/google/
  google-provider.ts              (CalendarProvider impl for Google)
  google-types.ts                 (Google-API-specific types)
  __tests__/google-provider.test.ts

src/lib/integrations/
  calendar-provider.ts            (CalendarProvider interface + canonical CalendarEvent)
  __tests__/calendar-provider.test.ts

src/lib/auth/
  envelope-encryption.ts          (AES-GCM envelope encryption helper)
  __tests__/envelope-encryption.test.ts

src/lib/domain/
  calendar-event.ts               (smart-default rules; series-exclusion resolution)
  __tests__/calendar-event.test.ts

src/lib/sync/
  calendar-sync.ts                (sync orchestrator — used by manual + cron paths)
  __tests__/calendar-sync.test.ts

src/lib/api/
  calendars.ts                    (Directus SDK wrapper for the 3 calendar collections + cron_monitor)
  __tests__/calendars.test.ts

src/lib/validation/
  calendar-binding.ts             (Zod schemas for route bodies + Google API responses)

src/app/api/calendars/google/connect/route.ts
src/app/api/calendars/google/callback/route.ts
src/app/api/calendars/[connection_id]/calendars/route.ts
src/app/api/calendars/[connection_id]/disconnect/route.ts
src/app/api/calendars/sync/route.ts
src/app/api/calendars/events/[id]/route.ts
src/app/api/calendars/events/[id]/include-series/route.ts
src/app/api/health/cron/route.ts

src/components/
  calendars-section.tsx           (Settings → Kalenders)
  choose-calendars-form.tsx       (post-OAuth calendar selection screen)
  calendar-event-sheet.tsx        (per-event detail BottomSheet)
  context-events-section.tsx     (Context tab events region)
  today-events-region.tsx         (Today card events region)
  timeline-event-markers.tsx      (timeline overlay)

directus/migrations/
  2026-XX-XX-calendar-binding-schema.sql

directus/scripts/
  setup-calendar-collections.mjs  (idempotent collection / field / relation creation)
  add-calendar-unique-constraints.mjs
  add-cron-monitor.mjs

.github/workflows/
  daily-calendar-sync.yml         (cron → POST /api/calendars/sync)
  cron-health-check.yml           (watchdog → poll /api/health/cron)

scripts/
  calendar-binding-smoke.mjs      (e2e prod smoke)
  calendar-cron-smoke.mjs         (cron round-trip prod smoke)
```

### Key types

```typescript
// src/lib/integrations/calendar-provider.ts
export interface CalendarProvider {
  id: 'google' | 'outlook' | 'apple';
  /** Build the OAuth authorization URL given a signed state cookie value. */
  buildAuthUrl(state: string, redirectUri: string): string;
  /** Exchange an auth code for tokens + the connection's account email. */
  exchangeCode(code: string, redirectUri: string): Promise<{ refreshToken: string; accessToken: string; expiresAt: Date; accountEmail: string }>;
  /** Refresh an access token from a stored refresh token. */
  refreshAccessToken(refreshToken: string): Promise<{ accessToken: string; expiresAt: Date }>;
  /** List the user's calendars (id + display name + colour). */
  listCalendars(accessToken: string): Promise<Array<{ id: string; displayName: string; isPrimary: boolean }>>;
  /** Fetch events in a bounded window from the included calendars. */
  fetchEvents(accessToken: string, includedCalendarIds: string[], from: Date, to: Date): Promise<CalendarEvent[]>;
  /** Revoke the OAuth grant. Best-effort; idempotent. */
  revoke(refreshToken: string): Promise<void>;
}

export interface CalendarEvent {
  providerEventId: string;
  recurrenceId: string | null;
  startAt: Date;
  endAt: Date;
  allDay: boolean;
  title: string;
  location: string | null;
  attendeesCount: number;
  declined: boolean;
}

// src/lib/api/calendars.ts — Directus row shapes (snake_case)
export interface DirectusCalendarConnectionRow {
  id: string;
  user_id: string;
  provider: 'google';
  provider_account_email: string;
  refresh_token_encrypted: string;  // envelope-encrypted; see envelope-encryption.ts
  scope: string;
  connected_at: string;
  last_synced_at: string | null;
  last_sync_error: string | null;
  status: 'active' | 'disconnected' | 'error';
  included_calendar_ids: string[];  // JSON array
}

export interface DirectusCalendarEventRow {
  id: string;
  connection_id: string;
  provider: 'google';
  provider_event_id: string;
  recurrence_id: string | null;
  start_at: string;
  end_at: string;
  all_day: boolean;
  title: string;
  location: string | null;
  attendees_count: number;
  declined: boolean;
  linked_tag_id: string | null;
  linked_episode_id: string | null;
  included_as_context: boolean;
  user_decision: 'auto' | 'user_included' | 'user_excluded';
  created_at: string;
  updated_at: string;
}

export interface DirectusCalendarSeriesExclusionRow {
  id: string;
  connection_id: string;
  recurrence_id: string;
  excluded_at: string;
}

export interface DirectusCronMonitorRow {
  id: string;
  job_name: string;
  last_run_at: string | null;
  last_result: string | null;
  expected_interval_hours: number;
  is_active: boolean;
}
```

### Integration with existing code

- Imports from `src/lib/api/`: pattern matches `tags.ts` / `episodes.ts` / `day-entries.ts`. Bulk `updateItems` / `deleteItems` for series operations per [src/lib/api/tags.ts](../../../src/lib/api/tags.ts) `mergeTag` precedent.
- Imports from `src/lib/auth/`: existing `getValidatedSession`, `parseSessionCookie`, `validateOrigin`. New `envelope-encryption.ts` adds AES-GCM helpers.
- Imports from `src/lib/validation/`: existing Zod-at-the-boundary pattern.
- Imports from `src/lib/integrations/`: this feature establishes the directory per REQUIREMENTS line 124.
- New hooks: none — the Settings / Context / Today flows use server components + form actions where possible. Per-event sheet uses an existing `useSession` pattern.
- Existing callers that change:
  - `src/lib/domain/episode.ts` (v1.6 → v1.6.1 comment update in step-0)
  - `src/lib/api/episodes.ts` (same)
  - `src/components/today-card.tsx` (add `today-events-region` import in step-2)
  - `src/components/context-view.tsx` (add `context-events-section` import in step-1)
  - `src/components/timeline-view.tsx` (add `timeline-event-markers` import in step-3)
  - `src/components/settings-view.tsx` (add `calendars-section` import in step-1)

---

## Steps

### Step 0: Data model migration + CalendarProvider interface + cron_monitor

- Migrate the v1 placeholder `calendar_events` to multi-provider shape (asserting empty).
- Create `calendar_connections`, `calendar_series_exclusions`, `cron_monitor` collections.
- Add UNIQUE constraints + indexes.
- Build `CalendarProvider` interface + canonical `CalendarEvent` shape (no implementation).
- Build envelope-encryption helper (encrypt / decrypt / round-trip tested).
- Add smart-default-rules domain function (`computeDefaultIncluded(event, seriesExclusions)`).
- Update stale `episodes.calendar_binding` v1.6 comments to v1.6.1.
- Extend `verify-schema.mjs` with new assertions.
- See: [step-0-data-model-and-provider.md](./step-0-data-model-and-provider.md)

### Step 1: Google OAuth + Settings + manual sync + Context tab

- OAuth connect / callback / disconnect routes.
- Calendar-list screen post-OAuth.
- Sync route (session-gated path).
- Settings → Kalenders surface.
- Context tab events section + per-event detail sheet + sluit-uit + series-include + tag/episode linking.
- The 3 smart-default rules applied at pull time.
- See: [step-1-google-oauth-and-context.md](./step-1-google-oauth-and-context.md)

### Step 2: Daily cron infrastructure + Today card

- GitHub Actions `daily-calendar-sync.yml` (cron trigger).
- Bearer-gated path of `/api/calendars/sync`.
- `cron_monitor` row write on every sync (success + failure).
- `GET /api/health/cron` endpoint.
- `cron-health-check.yml` watchdog.
- Today card events region.
- See: [step-2-daily-cron-and-today.md](./step-2-daily-cron-and-today.md)

### Step 3: Timeline overlay

- Timeline event-day markers (warm-earth tick above the score line).
- Multi-day event spans (faint bar layered behind the score line).
- Tap-marker → opens Context for that day.
- See: [step-3-timeline-overlay.md](./step-3-timeline-overlay.md)

### Step 4 (v2 defer marker): Learned rules

- See: [step-4-v2-learned-rules.md](./step-4-v2-learned-rules.md)

### Step 5 (v2 defer marker): Second provider (Outlook)

- See: [step-5-v2-second-provider.md](./step-5-v2-second-provider.md)

### Step 6 (v1.6.1 defer marker): Calendar-bound episodes

- See: [step-6-v1.6.1-calendar-bound-episodes.md](./step-6-v1.6.1-calendar-bound-episodes.md)

---

## Key files

### New files to create (full list in step files)

| File | Step | Contents |
|---|---|---|
| `src/lib/integrations/calendar-provider.ts` | 0 | Interface + canonical type |
| `src/lib/integrations/google/google-provider.ts` | 1 | Google impl |
| `src/lib/auth/envelope-encryption.ts` | 0 | AES-GCM helper |
| `src/lib/domain/calendar-event.ts` | 0 | Smart-default rules |
| `src/lib/sync/calendar-sync.ts` | 1, 2 | Orchestrator (manual + cron) |
| `src/lib/api/calendars.ts` | 0, 1 | Directus SDK wrapper |
| `src/lib/validation/calendar-binding.ts` | 1 | Zod schemas |
| `src/app/api/calendars/**/route.ts` | 1, 2 | Six routes |
| `src/app/api/health/cron/route.ts` | 2 | Watchdog endpoint |
| `src/components/calendars-section.tsx` | 1 | Settings surface |
| `src/components/choose-calendars-form.tsx` | 1 | Calendar selection |
| `src/components/calendar-event-sheet.tsx` | 1 | Per-event detail sheet |
| `src/components/context-events-section.tsx` | 1 | Context tab events |
| `src/components/today-events-region.tsx` | 2 | Today card events |
| `src/components/timeline-event-markers.tsx` | 3 | Timeline overlay |
| `directus/migrations/2026-XX-XX-calendar-binding-schema.sql` | 0 | Schema SQL |
| `directus/scripts/setup-calendar-collections.mjs` | 0 | Idempotent setup |
| `directus/scripts/add-calendar-unique-constraints.mjs` | 0 | Constraint adder |
| `directus/scripts/add-cron-monitor.mjs` | 0 | cron_monitor seeder |
| `.github/workflows/daily-calendar-sync.yml` | 2 | Cron workflow |
| `.github/workflows/cron-health-check.yml` | 2 | Watchdog workflow |
| `scripts/calendar-binding-smoke.mjs` | 1, 2 | Prod smoke |
| `scripts/calendar-cron-smoke.mjs` | 2 | Cron smoke |

### Files to modify

| File | Step | Change |
|---|---|---|
| `directus/scripts/setup-schema.mjs` | 0 | Migrate `calendar_events` placeholder to multi-provider shape; add 3 new collections |
| `directus/scripts/verify-schema.mjs` | 0 | Add assertions for new UNIQUE / FK / CHECK / column shapes |
| `src/lib/domain/episode.ts` | 0 | Update v1.6 → v1.6.1 comment on `calendar_binding` gate |
| `src/lib/api/episodes.ts` | 0 | Same |
| `src/components/settings-view.tsx` | 1 | Add Kalenders section import |
| `src/components/context-view.tsx` | 1 | Add events-section import + render |
| `src/components/today-card.tsx` | 2 | Add today-events-region import + render |
| `src/components/timeline-view.tsx` | 3 | Add timeline-event-markers import + render |

### Reference docs (patterns to extract from)

| Doc | What to extract |
|---|---|
| [features/tag-merge/step-1-tag-merge.md](../tag-merge/step-1-tag-merge.md) | Test-enumeration rigor; bulk SDK operations pattern; standard route auth stack |
| [features/tag-merge/step-0-junction-integrity.md](../tag-merge/step-0-junction-integrity.md) | SQL migration + verify-schema additions pattern; idempotent constraint setup |
| [features/tag-management-settings/](../tag-management-settings/) | BottomSheet picker pattern; Toon-overgeslagen toggle UX |
| [src/app/api/tags/[id]/merge/route.ts](../../../src/app/api/tags/[id]/merge/route.ts) | Standard route auth stack to mirror exactly |
| [src/lib/api/tags.ts](../../../src/lib/api/tags.ts) `mergeTag` | Bulk `deleteItems` / `updateItems` for series operations |
| [c:\Users\Gebruiker\Documents\programmeerprobeer\tvoo_frontend\src\app\api\health\cron\route.ts](c:\Users\Gebruiker\Documents\programmeerprobeer\tvoo_frontend\src\app\api\health\cron\route.ts) | `/api/health/cron` shape to port |
| [c:\Users\Gebruiker\Documents\programmeerprobeer\.github\workflows\cron-health-check.yml](c:\Users\Gebruiker\Documents\programmeerprobeer\.github\workflows\cron-health-check.yml) | Watchdog GHA shape to port |
| [c:\Users\Gebruiker\Documents\programmeerprobeer\.github\workflows\weekly-digest.yml](c:\Users\Gebruiker\Documents\programmeerprobeer\.github\workflows\weekly-digest.yml) | GHA-cron → Next.js endpoint pattern |

---

## Verification

### Automated

1. Tests: `npm test -- calendar`
2. Types: `npm run typecheck`
3. Lint: `npm run lint`
4. Verify gate: `npm run verify` (runs all of the above)
5. Schema verify: `node directus/scripts/verify-schema.mjs` (after each step's migration applied to prod)

### Manual

1. **Connect flow** in Safari iOS PWA: tap Verbind → Google consent → return → kies kalenders → submit → back in Settings, see connection row.
2. **Sync round-trip**: tap Ververs nu → spinner → updated `last_synced_at` → Context tab shows today's events.
3. **Per-event flow**: tap event in Context → sheet opens → link to tag → close → row updates.
4. **Series exclusion**: tap recurring event → Sluit uit als context → row disappears → Toon overgeslagen reveals it grey → tap series re-include → row reappears.
5. **Disconnect**: tap Ontkoppel → confirm → connection gone → events gone from Context / Today / Timeline.
6. **Brainfog walkthrough**: one-handed, low-light, arm's length. Sluit-uit must hit on first tap.
7. **Network-loss check**: DevTools Offline → Context still renders last-synced state → Ververs nu shows clear retry-able error.
8. **Export check**: CSV / JSON export includes events + connection metadata; excludes `refresh_token_encrypted`.
9. **Full-delete check**: trigger full wipe via Directus admin; confirm `calendar_connections` / `calendar_events` / `calendar_series_exclusions` are empty; confirm Google account dashboard shows the grant revoked.

### Testing strategy (new patterns introduced)

- **Encrypted-at-rest column testing.** New pattern for this codebase. Test that round-trip encrypt → decrypt works; that tampered ciphertext fails; that wrong KEK fails. Future encrypted columns (e.g. v2 reminder webhook tokens, if any) follow the same helper.
- **OAuth flow testing.** New pattern. Mock `fetch` to `accounts.google.com` + `oauth2.googleapis.com`. Test code-exchange, refresh, revoke separately.
- **Cron-trigger testing.** Mock the Next.js route call from the GHA workflow; verify the bearer gate; verify the cron_monitor row write. Production smoke (`scripts/calendar-cron-smoke.mjs`) closes the loop.
- **Multi-day event rendering.** New visual pattern in the timeline. Visual baseline snapshot per [.claude/testing.md](../../../.claude/testing.md) styling-baseline rule.

---

## Design insight: noise/signal is per-user, not algorithmic (2026-06-04)

During the pre-backfill curation step (after step-1 deploy, before the historical pull), the user reviewed 10 recurring series from the initial 37-day sample and elected to exclude ALL of them. The titles were a mix of single letters (`JM`, `W`), labelled appointments (`Datenight`, `Bestuurseten`), and Google auto-birthdays. There was no clean rule — in the user's own words:

> "this is not a clear pattern why, it is just calendar noise that i choose to ignore"

This validates the v1.6 design's choice to make exclusion a **manual per-series action** rather than a learned-rule or keyword-matched one. What looks like noise to one person ("birthday auto-reminders for distant contacts I haven't seen in a decade") may look like context to another ("social-connection density matters to my recovery"). The v1.6 design ships single-tap series exclusion in the UI; v2 may layer learned-rules on top of the captured `user_decision` signal, but the human's per-event call stays canonical. v1.6.x keyword rules (in the roadmap) are an opt-in shortcut for repeating patterns, not a replacement for the manual override.

A corollary: the `user_decision` field we ship in v1.6 ('auto' | 'user_included' | 'user_excluded') is doing more than tracking state. Every flip is a signal that future learned-rules (v2) could leverage, but the absence of a flip is ALSO signal — "the user left this alone" might mean "good enough" or "I haven't looked yet." Don't over-read either direction; the UI should make explicit decisions easy and forgiving.

## History

- 2026-06-03: Feature folder created. Four design conversations resolved:
  1. Surfaces (Settings / Context / Today / Timeline) + provider abstraction + event-tag separation + OAuth full-page redirect + calendar-level toggle + daily pull + 3 smart-default rules + series-default exclusion + three-state user_decision field
  2. Layered noise filter (calendar-level → per-event → keyword rules v1.6.x → learned v2)
  3. Stoplist removal (user correction on zero-duration / 0-attendee + the principle "blocks-to-do-work matter")
  4. Cron infrastructure pattern (GHA → Next.js → cron_monitor → /api/health/cron → watchdog GHA, ported from programmeerprobeer)

  Plus one in-plan decision: Shape A (event-side link) ships in v1.6; Shape B (episode-side binding) deferred to v1.6.1. Stale `episodes.calendar_binding` comment updates to v1.6.1 in step-0.
