# Step 5 (v2 — explicit defer marker): Second provider (Outlook / Apple)

**Status:** Deferred — v2.
**Trigger to graduate:** The user asks for it (single-user app; no abstract demand to model).
**Why deferred:** Each provider has its own OAuth flow + API shape + quirks (Outlook uses Microsoft Graph; Apple uses CalDAV which is dramatically different from REST). Building two providers in v1.6 would bloat scope without solving a known user need. The `CalendarProvider` interface from v1.6 step-0 is the seam that makes this cheap-to-add later.

---

## What this step would deliver

A second (or third) `CalendarProvider` implementation. UX is identical: connect → choose calendars → events flow through.

## Proposed shape

### For Outlook (Microsoft 365 / Outlook.com)

- `src/lib/integrations/microsoft/microsoft-provider.ts` implementing `CalendarProvider`.
- Microsoft Graph API: `https://graph.microsoft.com/v1.0/me/calendars` + `https://graph.microsoft.com/v1.0/me/calendars/{id}/events?$filter=...`.
- Scope: `Calendars.Read` (least privilege).
- OAuth via Microsoft Identity Platform v2.0 endpoint.
- New Fly + GHA secrets: `MICROSOFT_CLIENT_ID`, `MICROSOFT_CLIENT_SECRET`.

### For Apple (iCloud / Calendar)

- CalDAV protocol, NOT REST. Significantly different.
- `src/lib/integrations/apple/apple-provider.ts` — likely requires a small CalDAV helper.
- Apple app-specific passwords instead of OAuth.
- Skipped unless Outlook ships first and demand is clear.

### Schema impact

- `calendar_connections.provider` CHECK constraint widens from `('google')` to `('google', 'microsoft')`. One ADD CONSTRAINT migration via the existing pattern from v1.5d Tier 3.
- `calendar_events.provider` CHECK constraint same.
- No data migration needed (existing google rows stay valid).

### UX impact

- Settings → Kalenders empty-state shows both providers ungreyed: `[Verbind Google Calendar]` + `[Verbind Outlook Calendar]`.
- Connected state lists each connection with provider badge.

## Out of scope at trigger time

- CalDAV for Apple (defer further unless Outlook isn't sufficient).
- Pulling events from arbitrary `.ics` URLs (would need a separate "ICS calendar" provider; deferred until requested).
- Two-provider conflict resolution (same event in both Google and Outlook): single user, unlikely overlap; defer the design until soak data shows it matters.

## Acceptance criteria, technical constraints, and test plan

To be filled in when the trigger fires. Re-uses the v1.6 step-1 structure, swapping Google-specific routes for Microsoft-specific. The sync orchestrator (`src/lib/sync/calendar-sync.ts`) is provider-agnostic — no changes; only the provider implementation differs.

## Done

Not applicable until graduated.
