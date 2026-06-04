# Step 2: Daily cron + cron_monitor write + health endpoint + Today card

**Estimated time:** ~6 hours. Two GitHub Actions workflows, one new health endpoint, cron_monitor write in the sync route, one new Today card component.
**Test layers:** Vitest route tests for `/api/health/cron` (ports from programmeerprobeer's [route.ts](c:\Users\Gebruiker\Documents\programmeerprobeer\tvoo_frontend\src\app\api\health\cron\route.ts)); Vitest unit tests for `cron-monitor.ts` Directus wrapper (write-success-row + write-error-row); Vitest unit tests for the bearer-gate path of the sync route (extending step-1's route test file); component test for `TodayEventsRegion`; production smoke `scripts/calendar-cron-smoke.mjs` for the full GHA → sync → cron_monitor → health round-trip.
**Risk:** Medium. The GHA workflow is the first scheduled job in the repo; the watchdog is the alerting layer. Establishing both correctly is load-bearing for any future scheduled work.
**Prerequisite:** Step 1 complete. Sync route accepts both session and bearer gates. `cron_monitor` collection exists with the `daily_calendar_sync` row seeded (from step-0). `CALENDAR_SYNC_SECRET` Fly secret + GitHub Actions secret set (setup procedure in step-2.0 below).

> Step-2 wires the daily cron behind the bearer gate already shipped in step-1, plus adds the watchdog + health endpoint + Today card.

---

## Acceptance criteria

### cron_monitor write

- [ ] **AC2.1** `src/lib/api/calendars.ts` exports `recordCronRun(adminToken: string, jobName: string, result: { ok: true; details: object } | { ok: false; error: string }): Promise<void>`. Patches the row matching `job_name = jobName` to set `last_run_at = now` and `last_result = JSON.stringify(result).slice(0, 1000)` (1000-char hard cap to prevent log-equivalent disclosure of event data).
- [ ] **AC2.2** `result.details` for success contains ONLY counts + provider_event_ids: `{ connections: N, events_pulled: M, events_upserted: K, events_excluded_by_series: J }`. No event titles, no locations, no attendees.
- [ ] **AC2.3** `result.error` for failure is a short code (e.g. `'refresh_token_invalid'` or `'directus_unreachable'`). Never a stack trace, never the underlying error message verbatim.
- [ ] **AC2.4** Sync route calls `recordCronRun` for both session AND bearer paths (so manual `Ververs nu` ALSO updates the cron_monitor row — the row is "last sync, however triggered", which is the most useful interpretation for staleness checks).
- [ ] **AC2.5** `recordCronRun` failure does NOT propagate: the sync route's primary response still returns 200 with aggregate results even if the monitor write fails. The monitor failure is logged (short code, no PII).

### Route: health/cron

- [ ] **AC2.6** `GET /api/health/cron` exports a route handler. **No auth gate** (matches programmeerprobeer; the endpoint is a health check, intended to be polled by an unauthenticated watchdog). Response is JSON, no PII.
- [ ] **AC2.7** Reads `cron_monitor` via the existing scoped frontend token (or via a dedicated `CRON_MONITOR_READ_TOKEN` if the scoped token doesn't have read access to that collection — to be decided in build).
- [ ] **AC2.8** For each row, computes `status`:
  - `inactive` if `is_active = false`
  - `never_run` if `last_run_at = null` AND `is_active = true`
  - `stale` if `is_active = true` AND `last_run_at` is older than `expected_interval_hours`
  - `ok` otherwise
- [ ] **AC2.9** Returns `200 { status, timestamp, schedule, jobs: Array<{ jobName, lastRunAt, lastResult, status, hoursSinceRun }> }`. Overall `status = 'stale'` if any job stale, `'warning'` if any never_run, `'ok'` otherwise.
- [ ] **AC2.10** Returns `503` with `{ status: 'error', error }` if `cron_monitor` is unreachable (Directus down, etc.).
- [ ] **AC2.11** Response includes `Cache-Control: private, s-maxage=60` so polling tooling doesn't hammer the endpoint.
- [ ] **AC2.12** `lastResult` in the response surfaces the JSON-encoded string from `cron_monitor.last_result` BUT only counts + error codes per AC2.2/AC2.3 — by construction, the cron_monitor.last_result never contains PII so the health endpoint is safe to surface it.

### GHA workflow: daily-calendar-sync

- [ ] **AC2.13** `.github/workflows/daily-calendar-sync.yml` triggers on `cron: '0 3 * * *'` (03:00 UTC = 04:00 CET / 05:00 CEST) + `workflow_dispatch` for manual fire.
- [ ] **AC2.14** Single job, ubuntu-latest, timeout-minutes 5.
- [ ] **AC2.15** POSTs to `https://gevoelscore-frontend.fly.dev/api/calendars/sync` with `Authorization: Bearer ${{ secrets.CALENDAR_SYNC_SECRET }}` and `Content-Type: application/json`. Body `{}`.
- [ ] **AC2.16** Fails the workflow (non-zero exit) if HTTP status ≠ 200. Workflow failure → GitHub auto-emails maintainer.
- [ ] **AC2.17** Posts the response JSON to `$GITHUB_STEP_SUMMARY` for at-a-glance run review (counts only, no PII).
- [ ] **AC2.18** No `workflow_dispatch.inputs` complexity beyond `environment` (production / staging) — the route is the source of truth for sync behavior; the workflow is just the trigger.

### GHA workflow: cron-health-check

- [ ] **AC2.19** `.github/workflows/cron-health-check.yml` triggers on `cron: '0 */6 * * *'` (every 6 hours) + `workflow_dispatch`.
- [ ] **AC2.20** Polls `https://gevoelscore-frontend.fly.dev/api/health/cron`. No auth header (endpoint is unauthenticated per AC2.6).
- [ ] **AC2.21** Fails the workflow if HTTP status ≠ 200, OR if response `status` is `stale` or any job has status `never_run`. Workflow failure → GitHub email.
- [ ] **AC2.22** Posts a per-job status table to `$GITHUB_STEP_SUMMARY` matching programmeerprobeer's pattern.
- [ ] **AC2.23** Watchdog is the SOLE alerting layer. No SMS, no PagerDuty, no Slack, no email beyond GitHub's default. Single-user app; the maintainer's GitHub email is sufficient.

### Today card: events region

- [ ] **AC2.24** `src/components/today-events-region.tsx` rendered inside the existing `TodayShell` between the score region and the ongoing-episodes region (Activiteiten are a more immediate context than episodes; epidodes are slower-burning state).
- [ ] **AC2.25** Renders `calendar_events` overlapping today's date with `included_as_context = true`. Sorts by start_at ascending, all-day events first.
- [ ] **AC2.26** Each row: time + title + optional linked-tag badge.
- [ ] **AC2.27** Collapses to count when there are more than 3 events: shows the first 3 + `+ N meer` text-link → expands inline.
- [ ] **AC2.28** Empty state: no region rendered (no copy needed; saves space on the Today card).
- [ ] **AC2.29** Tap event row → opens the same `CalendarEventSheet` from step-1 (re-uses the component; no fork).
- [ ] **AC2.30** Loads events via a server component (matches the `today-card.tsx` pattern in the existing codebase). No client-side fetch / useEffect.

### Cross-feature integrity

- [ ] **AC2.31** Today card daily flow unaffected: tap-score still resolves in < 10s. The events region is below the score tap zone; it does not compete for the thumb area.
- [ ] **AC2.32** Loading the Today card with no events is unchanged (no new section visible).
- [ ] **AC2.33** GHA-triggered sync vs manual sync produce identical row writes (idempotent on UNIQUE).

---

## Technical constraints

- **Schedule: `0 3 * * *` UTC** (04:00 CET / 05:00 CEST). Chosen so a sync completes before the user wakes up; events fetched are fresh for the Today card on first view. Picks UTC over CET to avoid DST jumpiness (cron schedule moves by an hour twice a year if we use local time; UTC is stable).
- **Watchdog schedule: `0 */6 * * *` UTC.** Polls 4×/day. Stale-detection latency ≤ 6h after the breach. Stale threshold per job is `expected_interval_hours = 26` from step-0, so a missed daily sync surfaces within 6h after the 26h window closes (worst case: ~32h from prior success).
- **`CALENDAR_SYNC_SECRET` is a Fly secret + GitHub Actions secret.** Generated as 32-byte base64 random. Constant-time comparison via `crypto.timingSafeEqual`.
- **Health endpoint is unauthenticated.** Same posture as programmeerprobeer. The endpoint exposes job names + last-run times + result strings. By construction (AC2.2/AC2.3) the result strings carry no PII. The risk surface is low: an attacker learning "the daily calendar sync ran 5h ago and returned `{connections:1}`" gains nothing.
- **cron_monitor.last_result hard cap: 1000 chars.** Defensive. Prevents accidental log-equivalent disclosure if an error message ever leaks.
- **Today card uses a server component.** No client-side fetch. Matches the codebase pattern: server-side renders the Today card with day_entry data, episodes, and (now) events.
- **GHA workflows do NOT push commits or modify repo state.** Read-only on the repo; HTTP-only on the app. The "GHA staleness pause after 60 days" risk is documented in the README; mitigation is the watchdog (catches it) + the user's regular commit cadence on this app (keeps GHA active).

### Standards-enforcement declaration

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01, A03, A04, A07, A08 | Yes | `/api/health/cron` is unauthenticated by design (matches programmeerprobeer); no PII exposed by construction. |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | No | `cron_monitor` was created in step-0; this step writes to it but is otherwise infra metadata, not user data. |
| New dependency | ADR or step rationale | No | No new deps. GHA workflows use `curl` + `jq` (preinstalled on ubuntu-latest). |
| `dangerouslySetInnerHTML` usage | A03 | No | No new UI HTML rendering. |
| New env var with a secret | A02, A05 | Yes | `CALENDAR_SYNC_SECRET`: Fly + GHA secret. Never `NEXT_PUBLIC_*`. |
| New telemetry / observability dep | Cardinal "no telemetry" | No | GitHub's own email-on-failure is the entire alerting stack. |

---

## Test plan

### Directus wrapper: recordCronRun

**File**: `src/lib/api/__tests__/calendars.test.ts` (EXTEND)

Tests:

1. `recordCronRun` PATCHes the row matching `job_name` (AC2.1)
2. `recordCronRun` sets `last_run_at` to now (AC2.1)
3. `recordCronRun` sets `last_result` to JSON-encoded success (AC2.1, AC2.2)
4. `recordCronRun` truncates `last_result` to 1000 chars (AC2.1)
5. `recordCronRun` for failure stores `{ ok: false, error: <code> }` only (AC2.3)
6. `recordCronRun` failure (Directus unreachable) does NOT throw — logs and returns (AC2.5)

### Sync route: recordCronRun integration

**File**: `src/app/api/calendars/sync/__tests__/route.test.ts` (EXTEND from step-1)

Tests:

7. Session-path sync calls `recordCronRun` with success counts (AC2.4)
8. Bearer-path sync calls `recordCronRun` with success counts (AC2.4)
9. Sync route still returns 200 if `recordCronRun` fails (AC2.5)
10. Failure path: sync route calls `recordCronRun` with error code on per-connection failure (AC2.3)

### Route: health/cron

**File**: `src/app/api/health/cron/__tests__/route.test.ts`

Tests:

11. Returns 200 with `{ status, jobs[] }` shape (AC2.9)
12. No auth header required (AC2.6)
13. Job with fresh `last_run_at` → status `ok` (AC2.8)
14. Job with `last_run_at = null` → status `never_run`, overall `warning` (AC2.8, AC2.9)
15. Job with `last_run_at` older than `expected_interval_hours` → status `stale`, overall `stale` (AC2.8, AC2.9)
16. Job with `is_active = false` → status `inactive`, doesn't affect overall (AC2.8)
17. Mixed: one stale + one fresh → overall `stale` (AC2.9)
18. Mixed: one never_run + one fresh → overall `warning` (AC2.9)
19. Directus unreachable → 503 with `error` field (AC2.10)
20. Response includes `Cache-Control: private, s-maxage=60` (AC2.11)
21. `lastResult` surfaced verbatim (already PII-safe by construction) (AC2.12)

### Component: TodayEventsRegion

**File**: `src/components/__tests__/today-events-region.test.tsx`

Tests:

22. Renders events overlapping today with included_as_context=true (AC2.25)
23. Sorts by start_at ascending, all-day first (AC2.25)
24. Each row: time/Hele dag + title + optional tag badge (AC2.26)
25. 0 events: region not rendered (AC2.28)
26. 1-3 events: all rendered (AC2.27)
27. 4+ events: first 3 rendered + `+ N meer` text-link (AC2.27)
28. `+ N meer` click expands inline to show all (AC2.27)
29. Tap row opens CalendarEventSheet (AC2.29)
30. No client-side fetch; renders from props (AC2.30)

### GHA workflows

These are tested via execution, not Vitest. The Vitest suite covers the route code that the workflows POST to.

- **`daily-calendar-sync.yml`**: tested via `workflow_dispatch` in dev (manual trigger from GitHub UI). Verifies AC2.13-AC2.18.
- **`cron-health-check.yml`**: tested via `workflow_dispatch`. Verifies AC2.19-AC2.23.

### Production smoke

**File**: `scripts/calendar-cron-smoke.mjs`

End-to-end:

1. Read `cron_monitor.daily_calendar_sync.last_run_at` baseline (from Directus admin or via the health endpoint).
2. Trigger `daily-calendar-sync.yml` via `gh workflow run`.
3. Wait for workflow completion (~30s typical). Read `last_run_at` again — should be > baseline.
4. Read `last_result` — should be a JSON object with `connections` + `events_pulled` + etc, no PII.
5. Hit `GET /api/health/cron` directly — overall `status = 'ok'`, `daily_calendar_sync` job `status = 'ok'`.
6. Mutate the row (via Directus admin) to set `last_run_at` to 30h ago. Hit health endpoint again — overall `status = 'stale'`.
7. Trigger `cron-health-check.yml` via `gh workflow run`. Workflow should FAIL (the staleness propagates).
8. Reset `last_run_at` to now. Re-run watchdog — passes.

Total: **~30 enumerated tests** across 4 test files + 1 smoke. The GHA workflows themselves are tested by execution rather than unit tests.

---

## Done criteria

- [ ] Every AC GREEN
- [ ] RED + GREEN captured
- [ ] Full suite GREEN (no regressions; ~1233 + step-0's ~40 + step-1's ~119 + step-2's ~30 = ~1422 tests total)
- [ ] `npm run typecheck` / `npm run lint` / `npm run verify` clean
- [ ] `verify-schema.mjs` GREEN
- [ ] `CALENDAR_SYNC_SECRET` Fly secret + GHA secret confirmed set (names only)
- [ ] Daily-calendar-sync GHA fires successfully on `workflow_dispatch`
- [ ] Cron-health-check GHA passes on initial run
- [ ] Production smoke 8/8 GREEN
- [ ] No new HIGH gate findings
- [ ] Refactor pass complete

---

## Execution order

### 2.0 Setup (manual)

```powershell
# Generate the bearer secret
$secret = [Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))

# Set on Fly (the route reads it)
fly secrets set CALENDAR_SYNC_SECRET=$secret -a gevoelscore-frontend

# Set on GitHub Actions (the workflow uses it)
gh secret set CALENDAR_SYNC_SECRET --body "$secret"

# Do not echo $secret. Clear from session.
Remove-Variable secret
```

### 2.1 Baseline

Step-1 complete. Manual `Ververs nu` works. Production smoke from step-1 (10/10) GREEN.

### 2.2 Write tests (RED)

For each test file: stub the implementations (`recordCronRun` throws, route returns 500, etc), paste tests, run `npm test -- cron health today-events`, confirm failures.

### 2.3 Implement (GREEN)

Order:

1. `src/lib/api/calendars.ts` — `recordCronRun` function
2. Sync route extension — call `recordCronRun` in both paths
3. `src/app/api/health/cron/route.ts` — port from programmeerprobeer
4. `src/components/today-events-region.tsx`
5. Wire into `today-card.tsx`
6. `.github/workflows/daily-calendar-sync.yml`
7. `.github/workflows/cron-health-check.yml`

Run `npm test`, full suite GREEN.

### 2.4 Apply / deploy

```powershell
fly deploy -a gevoelscore-frontend
git add .github/workflows/daily-calendar-sync.yml .github/workflows/cron-health-check.yml
git commit -m "calendar-binding/step-2: GHA cron + watchdog"
git push origin main
```

GHA workflows become active on push.

### 2.5 Smoke

```powershell
# Trigger daily sync manually
gh workflow run daily-calendar-sync.yml

# Wait, then check cron_monitor + health endpoint
.\scripts\run-calendar-cron-smoke.ps1
```

### 2.6 Refactor

Common refactors:

- Hoist `cron_monitor` shape + `recordCronRun` into a `src/lib/api/cron-monitor.ts` if step-2's content in `calendars.ts` becomes muddled.
- Add `expected_interval_hours` constant to step-1's calendar-sync.ts if duplicated.
- Move the `Cache-Control` header default into the route helper.

### 2.7 Checkpoint

Commit message:

```
calendar-binding/step-2: daily cron + cron_monitor write + health endpoint + Today

GHA workflow daily-calendar-sync.yml fires at 03:00 UTC daily, POSTs to
/api/calendars/sync with Authorization: Bearer CALENDAR_SYNC_SECRET (set
on Fly + GitHub Actions). Sync route writes a cron_monitor row on success
and on failure (counts + error codes only, no PII; 1000-char cap).

GET /api/health/cron reads cron_monitor and reports per-job staleness.
Unauthenticated by design (no PII in response); ported from programmeerprobeer
(see tvoo_frontend/src/app/api/health/cron/route.ts). cron-health-check.yml
polls every 6 hours and fails the workflow (auto-emails maintainer) on stale
or never_run.

Today card gets a TodayEventsRegion above ongoing-episodes — surfaces today's
events with optional tag badge. Server component; no client fetch. Re-uses
the CalendarEventSheet from step-1 for per-event interaction.

Acceptance criteria addressed: AC2.1 through AC2.33 (33/33).

Tests: ~30 new tests across 4 files + 1 prod smoke. Full suite GREEN.
GHA dispatch round-trip 8/8 against gevoelscore-frontend.fly.dev.
```

---

## Done (filled in during `/build-step`)

- [ ] AC2.1-2.33: per test file mapping
- [ ] RED captured: ...
- [ ] GREEN captured: ...
- [ ] Type / lint / verify clean
- [ ] `CALENDAR_SYNC_SECRET` set on Fly + GHA
- [ ] daily-calendar-sync.yml fires on dispatch
- [ ] cron-health-check.yml passes initial run
- [ ] Smoke 8/8
- [ ] No new HIGH gate findings
- [ ] Refactor: ...

---

## What this step does NOT do

- **No timeline overlay.** Lands in step-3.
- **No alternate cron cadence.** Daily-only for now. Hourly or twice-daily would chew Google API quota (low concern) and burn extra GHA minutes (also low concern), but the daily cadence is the README's settled decision.
- **No alerting beyond GitHub email.** No SMS, no PagerDuty, no Slack, no in-app banner. Single-user app; the maintainer's GitHub inbox is sufficient.
- **No backfill of the cron_monitor.last_result for past runs.** The collection's rows accumulate as the cron fires; there's no migration of historical sync results.
- **No "Today card minus events" toggle.** If the user wants to hide the events region temporarily, they uncheck all calendars in Settings (rare; the per-event sluit-uit covers the per-event case).
