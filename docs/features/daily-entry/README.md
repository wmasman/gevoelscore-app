# Daily entry — Blok 1 (score) + Blok 2 (timeline)

**Feature:** The cardinal v1 product — one tap to log today's gevoelscore, optional note + tags, and a timeline that shows the patterns underneath. The audit-hardened auth layer is in place; this is what the auth was protecting.
**Version:** v1
**Status:** **Shipped 2026-05-28** — Steps 0 through 6 (incl. 4b redesign) committed on `main` + deployed to prod. In daily soak since. Step 4b's score row, the standalone `DayDetailSheet`, and `DayEntryEditor` were later removed when the [quick-entry-popout](../quick-entry-popout/) became the canonical daily-entry surface (Option A reconciliation, 2026-05-29).
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

**Blok 1 — Today (the daily wheel):**

- [ ] AC1: Opening `/` shows today's entry if one exists (`YYYY-MM-DD`, Europe/Amsterdam local date). If exists → wheel is positioned at the saved score and treated as "set". If not → wheel sits at idle default `5`, **not yet saved**.
- [ ] AC2: The score wheel is a vertical scroll-snap picker of values 1–10. Centred value = current selection. Scrolling, tapping a visible value, or arrow keys all change it.
- [ ] AC3: First *deliberate* interaction (scroll / tap / keypress) on a fresh day promotes the wheel's current value from "idle 5" to "saved" — fires PUT to `/api/day-entries/[today]` with that score. Subsequent changes debounce-save 500ms after the wheel settles on a new integer.
- [ ] AC4: Re-positioning to the same value that's already saved is a no-op (no wasted PUT).
- [ ] AC5: Buttons / wheel values are visually neutral — no red/green colour scale. The centred value has a single accent ring; everything else is plain.
- [ ] AC6: Note field is below the wheel. Free text, no length cap. Saves on blur or after 1.5s of typing-pause (whichever first); never on every keystroke. Note/tags edits are disabled until the wheel is promoted to "saved" on a fresh day.
- [ ] AC7: Tag chips are below the note, in a stack of **8 collapsed category headers** (mentaal / fysiek / overall / activiteit / gebeurtenis / interventie / project / custom). Tap a header to expand its chips inline; tap again to collapse. Multiple categories can be open at once (don't punish exploration).
- [ ] AC8: Tapping a chip toggles its inclusion in `tag_ids` and fires an immediate PUT with the updated array. Optimistic update + revert on error.
- [ ] AC9: Network failure on any save shows a small, non-blocking error ("Niet opgeslagen — probeer nogmaals") near the affected control. State reverts to the last server-confirmed value.
- [ ] AC10: The wheel + collapsed tag stack fit on a phone screen without scrolling (the wheel itself is the only scrollable element). Touch targets ≥ 44px. Tested one-handed, arm's length, low light.
- [ ] AC11: Total flow on a good-day simulation (open app → scroll wheel to 7 → close): ≤ 5 seconds stopwatch-verified.

**Blok 2 — Timeline:**

- [ ] AC12: A swipe (or tap on a tab) reveals the timeline view. Default range: last 30 days.
- [ ] AC13: The chart shows a single line, x-axis = date, y-axis = score (1–10). Missing days are visible as gaps (no interpolation that lies about data).
- [ ] AC14: A toggle switches between 30-day and 90-day ranges. Loads from the server lazily — the 90-day view only fetches when first opened.
- [ ] AC15: Streak counter shows consecutive days logged (ending today or yesterday if today not yet logged). Resets visibly on a gap.
- [ ] AC16: Tapping any day (logged or missing) opens an **editable** bottom sheet for that date, with the same score wheel + note + tags components as Blok 1. Save semantics identical to Blok 1.
- [ ] AC17: A day whose `updated_at` is meaningfully later than `created_at` (heuristic: > 1 day apart) gets a subtle `bewerkt` marker on its tooltip + bottom-sheet header. Self-awareness without judgment; not an audit log.
- [ ] AC18: Timeline accommodates the 1,363 days already in the database without performance degradation. The 90-day query reads ≤ 90 rows; 30-day reads ≤ 30. No client-side filtering of larger payloads.

**Auth + security:**

- [ ] AC19: All `/api/day-entries` routes require a valid session cookie (via `getValidatedSession`). Middleware already gates `/api/*` since step 7 of auth-hardening (M2 fix).
- [ ] AC20: Body validation on POST/PATCH uses domain-layer validators (`validateScore`, `validateNote`, `validateTagIds`, `validateDate`). Anything that doesn't pass returns 400 with a generic `invalid_request` — no field-by-field error leaks.
- [ ] AC21: Origin check on every state-changing route. Rate limit by IP at the standard 5/5min (creating 5 entries per 5 minutes per IP is plenty for a single user; abuse is the threat model).
- [ ] AC22: GET routes are not rate-limited (read traffic is the happy path; rate limiting reads on a single-user app is theatrical).

## Component architecture (shared primitives)

Three patterns recur across Steps 4–6. Naming them now prevents drift.

### Shared hook: `useDayEntryUpsert(date)`

Lives at [`src/hooks/use-day-entry-upsert.ts`](../../../src/hooks/use-day-entry-upsert.ts). Returns:

```ts
{
  save: (patch: Partial<DayEntryPatch>) => Promise<void>;
  status: 'idle' | 'saving' | 'saved' | 'error';
  lastError: string | null;
}
```

Encapsulates: AbortController-cancel of in-flight requests, optimistic-update revert on failure, 500ms settle debounce when called rapidly. Every component that mutates a day_entry calls this — wheel, note, each tag toggle. **Introduced in Step 4** (where it has its first caller); reused by Steps 5 and 6.

### Shared component: `<SaveStatus />`

Lives at [`src/components/save-status.tsx`](../../../src/components/save-status.tsx). Props: `status: 'idle' | 'saving' | 'saved' | 'error'; error?: string | null`. Renders:

- `idle`: nothing
- `saving`: small "…" indicator
- `saved`: green check + brief fade (800ms)
- `error`: red banner "Niet opgeslagen — probeer nogmaals" with retry handler from props

One source of truth for the save-state visual language. Introduced in Step 4 alongside the hook.

### Shared composite: `<DayEntryEditor />`

Lives at [`src/components/day-entry-editor.tsx`](../../../src/components/day-entry-editor.tsx). Props: `date: string; initialEntry: DayEntry | null; allTags: Tag[]`. Renders the wheel + note + collapsed tag stack as a vertical unit.

Used twice:
- **Step 2 / Step 4 / Step 5**: as the main body of the Today screen.
- **Step 6**: inside the timeline's bottom sheet (with `date` being the tapped day).

Introduced in Step 5 (after wheel + note + tags all exist as parts).

### What deliberately is NOT shared (yet)

- **`<ScoreWheel />`, `<NoteField />`, `<TagPicker />`** stay as individual components inside `DayEntryEditor`. Splitting them lets each step test in isolation and lets future surfaces (settings? imports?) reuse a single piece if needed. No premature abstraction beyond that.
- **No design-system / button primitive layer.** Tailwind utility classes are the design system for v1. A `<Button>` primitive lands when a third surface (settings, import UI) actually needs it.
- **No theming / token layer.** Single user, no dark-mode toggle in v1.

This three-tier shape (hook → status component → composite) is the smallest abstraction that closes the duplication the steps would otherwise carry. Verified against /build-step's "don't add abstractions for single-use code" rule: each shared piece has 3+ anticipated call sites in the same feature.

## Accessibility target (project-wide standard)

**Formal target: WCAG 2.2 Level AA.** Enforced by `eslint-plugin-jsx-a11y` (lint), `@axe-core/playwright` (e2e), and a manual keyboard + VoiceOver walkthrough per step.

**Brainfog extensions** (above WCAG, specific to Long COVID cognitive symptoms):

| Brainfog rule | WCAG floor | Project target |
|---|---|---|
| Touch targets | 24×24 (AA), 44×44 (AAA) | ≥ 48×48 |
| Body text size | 16px implied | ≥ 17px @ default zoom, line-height ≥ 1.5 |
| Animation duration | No specific rule | ≤ 200ms; respect `prefers-reduced-motion` |
| Information density | No specific rule | Max 5 primary actions visible at once on the daily screen |
| Time pressure | SC 2.2.1 (adjustable timers) | No timers at all on user-facing flows |

**Specific WCAG 2.2 SCs needing explicit attention per step** (the rest fall out of jsx-a11y + axe):

- 1.4.3 Contrast (Min) 4.5:1 — enforced via CSS tokens chosen in Step 0
- 1.4.10 Reflow — usable at 320px width with no horizontal scroll
- 2.1.1 Keyboard — wheel + tag picker + bottom sheet all keyboard-operable
- 2.4.3 Focus Order — logical (wheel → note → tags; in sheet: same)
- 2.4.7 Focus Visible — `:focus-visible` ring on every interactive element
- 2.5.5 Target Size — ≥ 48 (above AA's 24×24)
- 3.3.1 Error Identification — covered by `<SaveStatus />`
- 4.1.2 Name, Role, Value — wheel needs `role="spinbutton"` + `aria-valuenow/min/max`; sheet needs `role="dialog"` + focus trap

The policy lives in [`docs/architecture/frontend-conventions.md`](../../architecture/frontend-conventions.md) (created by Step 0).

## Technical constraints

- **Domain layer is locked.** Routes consume the existing validators in [src/lib/domain/](../../../src/lib/domain/); no schema changes.
- **Directus schema is deployed.** The `day_entries`, `tags`, `day_entries_tags` collections exist and are populated. No `directus/scripts/` changes for v1.
- **No new dependencies.** The chart library and any state management are TBD per step file — but the bar is high: each new dep needs an ADR or rationale per the standards-enforcement table.
- **PWA shell** is in scope but not the *install* flow. The app should work as a website that happens to be installable; the prompt-to-install flow is post-v1.
- **Audit log INSERT placeholder**: every POST/PATCH/DELETE handler carries a `// TODO(I3): audit-log entry` comment for the future Track A3 backfill. No log infrastructure now (deferred to pre-launch).
- **Timeline performance**: 90 rows max per request. Use the existing `daily_observations` view if it lands first, or a direct Directus REST query otherwise. Decided per step file.

## Steps

0. **[Step 0 — Frontend foundation](step-0-frontend-foundation.md)** — `cn()` + `copy.ts` + CSS tokens + `next/font` + viewport/theme-color meta + `eslint-plugin-jsx-a11y` + `@axe-core/playwright` + `error.tsx` / `not-found.tsx` / `loading.tsx` + `docs/architecture/frontend-conventions.md`. Prerequisite for every UI step. Steps 1 + 3 (pure backend) can run independently of this.
1. **[Step 1 — `/api/day-entries` read API](step-1-day-entries-read-api.md)** — GET `/api/day-entries?from=X&to=Y` + GET `/api/day-entries/today`. Read-side first so the timeline can hook into real historical data without any UI for writes yet.
2. **[Step 2 — Today screen shell](step-2-today-screen-shell.md)** — Auth-gated server component renders the wheel (in idle state) + collapsed-tag stack. Uses the Step 0 foundation. No save logic yet; establishes layout + data path.
3. **[Step 3 — `/api/day-entries` write API](step-3-day-entries-write-api.md)** — PUT `/[date]` upsert (covers both today and any past date for timeline editing). Origin check + rate limit + body validation per AC19–21.
4. **[Step 4 — Score wheel UI + shared hook/status](step-4-score-tap-ui.md)** — Wheel + introduces `useDayEntryUpsert(date)` + `<SaveStatus />` (the shared primitives Steps 5 + 6 reuse). AC1–AC5, AC9–AC11. *Initially shipped as a vertical scroll-snap wheel; redesigned to a horizontal row in [Step 4b](step-4b-score-row-and-save-relocation.md). **Superseded 2026-05-29 by [quick-entry-popout/](../quick-entry-popout/) — the home / Today tab now uses the thumb-zone popout. `ScoreRow` was removed at that point.*** 
4b. **[Step 4b — Score row redesign + save-status relocation](step-4b-score-row-and-save-relocation.md)** — Post-ship redesign of Step 4 to match the locked design at [docs/design/brief.md](../../design/brief.md): vertical wheel → horizontal row, `<SaveStatus />` moves from inside the score component to the page header. Component renamed `score-wheel` → `score-row`. *Superseded 2026-05-29 by `quick-entry-popout/` Step 4 (Option A reconciliation). `ScoreRow` was removed; the page-header `<SaveStatus />` glyph was removed (the popout's end-of-flow card-pulse is the success signal). The error banner remains.*
5. **[Step 5 — Note + tag-category list + composite](step-5-note-and-tags-ui.md)** — Note debounce + 4 primary category headers + "Extra opties" collapse revealing the 4 remaining categories. AC6–AC8. *`<NoteField>` and `<TagCategoryList>` survived the 2026-05-29 reconciliation and are now consumed by [`QuickEntryFlow`](../quick-entry-popout/step-3-quick-entry-flow.md) on the note + tags steps. The `<DayEntryEditor />` composite was removed.*
6. **[Step 6 — Timeline (Blok 2) with editable bottom sheet](step-6-timeline-blok2.md)** — Chart + streak + tap-any-day-to-edit bottom sheet. AC12–AC18. `bewerkt` marker for edited days. Chart-lib decision lives here. *2026-05-29: the standalone `<DayDetailSheet>` was removed; tapping a chart point or heatmap cell now opens the same `<QuickEntryFlow>` popout with `isPastDay=true`. Consistent edit surface across home and timeline.*

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
| No unsolicited notifications / ads / analytics | Enforced | ESLint `no-restricted-imports` blocks Sentry/PostHog/Vercel Analytics |
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
