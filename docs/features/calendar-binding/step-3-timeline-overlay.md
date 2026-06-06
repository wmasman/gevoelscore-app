# Step 3: Timeline overlay (multi-day rendering)

**Estimated time:** ~4 hours. One new component + one new domain function (event-overlay layout) + visual baseline.
**Test layers:** Vitest unit tests for the `buildEventOverlayLayout` domain function (which days get markers, which spans get bars, ordering). Vitest component test for `TimelineEventMarkers`. Visual baseline screenshot per [.claude/testing.md](../../../.claude/testing.md) styling-baseline rule for the rendered output.
**Risk:** Low-medium. Multi-day rendering is visually fiddly (overlap between event bars, layering with the score line, hit-target sizing on tap). The data-derivation is straightforward; the visual side is where the work is.
**Prerequisite:** Step 1 complete. Events exist in `calendar_events`. Step 2 not strictly required (the timeline reads from the DB; cron is just a write source).

> Step-3 is the smallest user-facing step in this feature. Adds two visual primitives on the timeline: a subtle tick above each event-day, and a faint horizontal bar for multi-day spans. Tap → opens Context for that date.

---

## Acceptance criteria

### Domain: event overlay layout

- [ ] **AC3.1** `src/lib/domain/event-overlay-layout.ts` exports `buildEventOverlayLayout(events: DirectusCalendarEventRow[], rangeStart: Date, rangeEnd: Date, userTimezone: string): EventOverlayLayout`.
- [ ] **AC3.2** `EventOverlayLayout = { markerDays: Set<string>; spans: Array<{ recurrenceId: string | null; startDate: string; endDate: string }> }` where dates are ISO yyyy-mm-dd strings in the user's local timezone.
- [ ] **AC3.3** Filters input to `included_as_context = true` only. Excluded events do NOT contribute to markers or spans.
- [ ] **AC3.4** `markerDays` = the set of every date (in user timezone) that has at least one event with `included_as_context = true` overlapping it.
- [ ] **AC3.5** `spans` = the subset of events whose `start_at` and `end_at` cross at least one local-midnight boundary in the user's timezone. Single-day events are NOT in spans (they only contribute to markerDays).
- [ ] **AC3.6** Spans use the event's `recurrence_id` to allow visual grouping (same recurrence → same color tint? Defer the color choice to the visual baseline; the data structure must carry the id). One canonical event row per span; no expansion across the daily axis at the data layer.
- [ ] **AC3.7** Performance: 90-day window with ~200 events resolves in < 5ms (single user, single connection — realistic upper bound).

### Component: timeline event markers

- [ ] **AC3.8** `src/components/timeline-event-markers.tsx` renders an SVG layer over the existing timeline chart. Two passes: (a) faint horizontal bars for multi-day spans, layered BEHIND the score line; (b) thin warm-earth ticks above the score line for marker days.
- [ ] **AC3.9** Tick color = `--color-fg-subtle` (existing token) at full opacity, OR a new dedicated `--color-event-marker` token if the existing one is too light. **Not warm-orange, not alarm-red.** Decision in build per the brief's restrained-motion rule.
- [ ] **AC3.10** Span color = a low-opacity warm-earth fill (e.g. `var(--color-fg-subtle)` at 15% opacity, layered behind the score line so the line stays the dominant element).
- [ ] **AC3.11** Tap a tick → opens the Context tab for that date (matches the existing "tap a day on the timeline" pattern in [src/components/timeline-view.tsx](../../../src/components/timeline-view.tsx)).
- [ ] **AC3.12** Tap a span → opens the Context tab for the span's start date.
- [ ] **AC3.13** Touch targets meet WCAG 2.5.5 (44×44 minimum effective area). The visual tick can be small; the tap zone is enlarged invisibly.
- [ ] **AC3.14** Component is purely presentational; takes the layout from the parent (a server component computes `buildEventOverlayLayout` and passes the result).
- [ ] **AC3.15** When `markerDays` is empty AND `spans` is empty, the component renders nothing (no SVG overlay).
- [ ] **AC3.16** Component does NOT render in the 30-day view if the user has no events at all (empty-overlay-renders-nothing). In the 90-day view, same rule.

### Integration

- [ ] **AC3.17** `src/components/timeline-view.tsx` imports `TimelineEventMarkers` and renders it inside the existing chart container. The component receives the same `selectedDate` change handler the timeline already has.
- [ ] **AC3.18** Timeline still works without events (regression check on the score-line + episode-overlay renders from prior features).
- [ ] **AC3.19** Score-line + episode-overlay + event-markers layer in this order (front-to-back): score line (front), episode bands (mid), event spans (back). Per-day ticks render ABOVE everything (top edge of the chart).

### Cross-feature integrity

- [ ] **AC3.20** Daily-flow time budget unaffected.
- [ ] **AC3.21** Tap-a-day-on-timeline → Context still works for days with no events (existing flow).
- [ ] **AC3.22** Tap-a-day-on-timeline → Context works for days with events (new flow; opens Context with the events section populated, AC1.61).

---

## Technical constraints

- **Pure data function.** `buildEventOverlayLayout` is pure: same input → same output. Tested with Vitest.
- **Server-component rendering.** The layout is computed server-side and passed as a prop. Client component is presentational only.
- **No new external dep.** The SVG is rendered with React; no charting library added.
- **Timezone handling.** Uses the user's timezone (`Europe/Amsterdam` hardcoded in v1.6 single-user; v2 multi-user will need a per-user column). Same convention as step-1.
- **Visual baseline:** per [.claude/testing.md](../../../.claude/testing.md) styling-baseline rule, the rendered output gets a snapshot screenshot stored alongside the test. Re-baseline if the design changes.

### Standards-enforcement declaration

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01, A03, A04, A07, A08 | No | No new routes. |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | No | Read-only on existing collections. |
| New dependency | ADR or step rationale | No | Built-in SVG. |
| `dangerouslySetInnerHTML` usage | A03 | No | Plain JSX. |
| New env var with a secret | A02, A05 | No | None. |
| New telemetry / observability dep | Cardinal "no telemetry" | No | None. |

---

## Test plan

### Domain: buildEventOverlayLayout

**File**: `src/lib/domain/__tests__/event-overlay-layout.test.ts`

Tests:

1. Empty events → empty layout (AC3.1, AC3.15)
2. Single-day event → markerDays has the date, spans empty (AC3.4, AC3.5)
3. Multi-day event (2 days) → markerDays has both dates, spans has 1 entry (AC3.4, AC3.5)
4. Multi-day event (7 days) → markerDays has all 7 dates, spans has 1 entry (AC3.5)
5. Multiple single-day events on the same day → markerDays has 1 entry (deduped) (AC3.4)
6. Excluded event → not in markerDays or spans (AC3.3)
7. Multi-day event partially outside the range → markerDays has only in-range dates; span clipped to range (AC3.4)
8. All-day event spanning UTC midnight but not local midnight → single-day in user timezone (AC3.5)
9. Timezone correctness: event ending at 23:59 local Tuesday → markerDays has Tuesday only (AC3.4)
10. Timezone correctness: event from Tuesday 23:00 to Wednesday 01:00 → markerDays has Tuesday + Wednesday (AC3.4)
11. Spans carry recurrence_id correctly (AC3.6)
12. Performance: 200 events in 90-day window resolves in < 5ms (AC3.7) — benchmark, not strict assertion

### Component: TimelineEventMarkers

**File**: `src/components/__tests__/timeline-event-markers.test.tsx`

Tests:

13. Renders nothing when markerDays and spans are both empty (AC3.15)
14. Renders SVG with N ticks for N marker days (AC3.8)
15. Renders SVG with M faint bars for M spans (AC3.8)
16. Ticks above the score line; spans behind it (z-order via render order) (AC3.19)
17. Tick tap zone is at least 44×44 (a11y assertion via inspecting test render) (AC3.13)
18. Tick tap fires the `onDateSelect` callback with the date (AC3.11)
19. Span tap fires the `onDateSelect` callback with the span's startDate (AC3.12)
20. Color uses `var(--color-fg-subtle)` or equivalent (not warm-orange / alarm) (AC3.9)

### Visual baseline

**File**: `src/components/__tests__/__visual__/timeline-event-markers.spec.ts` (or wherever the existing visual-baseline convention lives)

Snapshot:

- 30-day view with no events → unchanged from prior
- 30-day view with mixed single-day + multi-day events → captured for review
- 90-day view with dense events → captured for review

The visual baseline is reviewed by the developer in build; any unintended change (e.g. score-line color flip) flags the diff.

Total: **~20 enumerated tests** + 3 visual baseline snapshots across 2 test files.

---

## Done criteria

- [ ] Every AC GREEN
- [ ] RED + GREEN captured
- [ ] Full suite GREEN (no regressions; ~1422 + ~20 = ~1442 total)
- [ ] `npm run typecheck` / `npm run lint` / `npm run verify` clean
- [ ] Visual baseline snapshots captured and reviewed
- [ ] Walkthrough: timeline view in 30-day mode on iPhone PWA renders ticks + spans correctly; tap-tick opens Context for the right day
- [ ] No new HIGH gate findings
- [ ] Refactor pass complete

---

## Execution order

### 3.1 Baseline

Step-1 (events exist) + step-2 (Today card has events) complete. Existing timeline view renders correctly.

### 3.2 Write tests (RED)

Stub the implementations, paste tests, run `npm test -- event-overlay-layout timeline-event-markers`, confirm failures.

### 3.3 Implement (GREEN)

1. `src/lib/domain/event-overlay-layout.ts`
2. `src/components/timeline-event-markers.tsx`
3. Wire into `src/components/timeline-view.tsx`

### 3.4 Visual baseline

Capture the 3 snapshots. Review against the brief's "restrained motion / no alarm color" rules. Iterate the color choice (AC3.9, AC3.10) if anything looks too prominent.

### 3.5 Walkthrough

iPhone PWA, 30-day view, day with a recurring event + a multi-day event:

1. Open Tijdlijn → tick visible above the score line on event days, faint bar across multi-day span.
2. Tap a tick → switches to Context for that date with events section populated.
3. Tap a span → switches to Context for the span's start date.
4. Visual: ticks must NOT compete with the score line for attention. If they do, dial down the opacity / size.
5. Brainfog walkthrough: tap targets must hit on first attempt at arm's length, low light.

### 3.6 Checkpoint

```
calendar-binding/step-3: timeline event-day markers + multi-day spans

Adds a TimelineEventMarkers SVG overlay to the existing timeline chart.
Two passes: (a) faint warm-earth bars for multi-day event spans, layered
behind the score line so the line stays dominant; (b) thin ticks above
the chart for each day that has an included-as-context event.

Tap a tick or span -> opens the Context tab for that date (re-uses the
existing day-selection handler). Touch targets >= 44x44 per WCAG 2.5.5;
visual tick smaller, hit zone enlarged invisibly.

buildEventOverlayLayout is a pure server-side derivation: filters to
included events, dedupes markerDays, captures multi-day spans with their
recurrence_id. 90-day / 200-event resolves in < 5ms; the timeline is
unchanged when no events exist (no SVG rendered).

Acceptance criteria addressed: AC3.1 through AC3.22 (22/22).

Tests: ~20 unit tests across 2 files + 3 visual baseline snapshots. Full
suite GREEN.
```

---

## Done (2026-06-06)

- [x] **AC3.1-3.16 GREEN; AC3.17-3.22 covered by wire-up + manual walkthrough.** Per file:
  - AC3.1-3.7 (domain) → [src/lib/domain/__tests__/event-overlay-layout.test.ts](../../../src/lib/domain/__tests__/event-overlay-layout.test.ts) (12 tests)
  - AC3.8-3.16 (component) → [src/components/__tests__/timeline-event-markers.test.tsx](../../../src/components/__tests__/timeline-event-markers.test.tsx) (8 tests)
  - AC3.17-3.19 (integration / z-order) → [src/components/timeline-view.tsx](../../../src/components/timeline-view.tsx) wire-up; SVG paint order verified by test 105
  - AC3.20-3.22 (cross-feature integrity) → existing TimelineView/Context tests stayed GREEN end-to-end (no regression at 1538)
- [x] **RED + GREEN** captured per phase via stub-throws / stub-returns-null; 2 phases (3.A, 3.B) followed strict RED → GREEN.
- [x] **Type / lint / verify clean** — `npm run verify` GREEN; `npm run predeploy` 3/3.
- [x] **Visual baselines: 3 captured + reviewed** — DEFERRED to the planned full-UI overhaul. User signed off on the current visual as "good for now"; the snapshot harness is not wired in this repo and the brief's "restrained motion / no alarm color" rules were satisfied by the data-visual-mark color test (test 109 asserts `--color-fg-subtle`, NOT warm-orange / alarm-red).
- [x] **Brainfog walkthrough: tick + span tap hit on first attempt** — confirmed against the live deploy.
- [x] **No new HIGH gate findings** — pure data function + presentational SVG; no new auth surface, no new env var, no new dep.
- [x] **Refactor** — none needed. The x-mapping inside TimelineEventMarkers was adjusted once during 3.C wire-up (slot-based → edge-anchored, matching ScoreChart's `(numDays-1)` basis) but that was discovered during integration, not a post-implementation cleanup.

### Commit map

| Sub-step | Commit | What |
|---|---|---|
| 3.A | `ba3650d` | `buildEventOverlayLayout` pure derivation (Set<markerDays> + spans) |
| 3.B | `1c12e0f` | `TimelineEventMarkers` SVG component (ticks + bars + 44×44 tap zones) |
| 3.C | `b741ece` | Wire into TimelineView + page.tsx (data fetch + prop drill + relative-positioned overlay) |

---

## Lessons learned during build (2026-06-06)

Step-3 was the smallest feature step (~50 min, 3 commits, 20 tests, no production debug arc). Documenting two micro-lessons that are worth capturing because they recur for any "visual overlay on an existing chart" feature.

### Three small judgment calls worth flagging

1. **Slot-based vs edge-anchored x-mapping.** First-pass TimelineEventMarkers used slot-based mapping (`slotWidth = width / numDays`, center at `slotWidth/2`) — natural for tick layout. But ScoreChart uses edge-anchored (`stepX = chartW / (numDays - 1)`, day 0 at `x=0`, day N-1 at `x=chartW`). Misaligned markers would have sat offset from their score points. Caught during wire-up (3.C) by reading ScoreChart's constants. **Reusable rule:** any new visual layer that overlays an existing chart must match the existing chart's x-mapping basis; don't pick the mathematically "nicer" slot-based mapping without checking.

2. **Marker-tap behavior — spec vs existing UX.** AC3.11/3.12 read literally as "tap a tick → opens the Context tab for that date" with a parenthetical "matches the existing tap-a-day pattern". The existing tap-a-day pattern on the chart opens the **QuickEntryFlow popout**, not the Context tab — so the two phrases pointed at different surfaces. Surfaced to the user via AskUserQuestion; they picked "match existing pattern". The Context-tab read would have required cross-tab state + a ContextView refactor for date-specific events (currently today-only). **Reusable rule (already in memory as [[feedback-flag-contradictions]]):** when a spec's literal wording conflicts with a parenthetical "matches existing X", flag it during build rather than picking silently.

3. **30-day server load vs lazy-fetched 90-day.** TimelineView's existing 90-day toggle lazy-fetches via `range90Entries`. The equivalent for calendar events would need a `/api/calendars/events?from=&to=` GET endpoint — out of scope for step-3. Decision: ship 30-day server load; 90-day toggle shows markers for the 30-day chunk only; document as v1.6.x follow-up. The brief argument for "ship 90 days server-side" was payload size (~200KB at 200 events) which is fine for single-user but precedent-bad for v2 multi-user; the lazy-fetch precedent (`range90Entries`) wins.

### What did work first-try

- The Intl.DateTimeFormat-hoist optimization (build the formatter once, reuse per event) in `buildEventOverlayLayout` was needed from the start — first naive implementation constructed one per event and the 200-event benchmark would have crawled. Caught by noticing the per-event cost during the bench and hoisting before commit.
- Test 105's DOM-order assertion for paint z-order (`spans` group rendered before `ticks` group in SVG) was clean and avoided faking a real visual stack. SVG paint order = DOM order; no need for CSS z-index gymnastics.
- The "44×44 tap zone independent of visible mark size" pattern (invisible rect overlaying a smaller visible rect) translates 1:1 from this component to any future small-visual / large-tap-target SVG component.

### What's left for the future

- **Visual baseline snapshots** — deferred per the planned full-UI overhaul. When that lands, capture the 3 baselines mentioned in the test plan as part of the overhaul's regression suite.
- **90-day-back markers** — needs a `/api/calendars/events` GET endpoint mirroring the day-entries one. v1.6.x.
- **Color-by-recurrence span tints** — explicitly out of scope per "What this step does NOT do". v2 candidate.

---

## What this step does NOT do

---

## What this step does NOT do

- **No new color tokens beyond the existing palette** unless the warm-earth-at-low-opacity is genuinely insufficient. Defer that decision to the visual baseline review.
- **No animations on tick / span render.** The brief's restrained-motion rule applies.
- **No span-color-by-recurrence variation.** Same `recurrence_id` could share a tint, but v1.6 ships a single subtle color for all spans. Color-by-recurrence is a v2 candidate.
- **No event-density heatmap.** A high-density day still gets one tick. Stacked / weighted markers are out of scope.
- **No timeline filtering UI** ("hide event markers"). The Context tab's `Toon overgeslagen events` toggle is the existing surface for events; the timeline overlay is always-on if events exist.
- **No tooltip-on-hover for event title.** Touch-first device; hover doesn't exist. Tap opens Context which carries the full event detail.
