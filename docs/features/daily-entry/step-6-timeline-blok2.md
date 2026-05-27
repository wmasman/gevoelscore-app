# Step 6: Timeline (Blok 2) — 30/90-day chart + streak counter

**Estimated time:** 3 hours (largest step in the feature)
**Test layer:** Vitest component (jsdom) for the streak math + Playwright e2e for the swipe + chart interaction + a manual visual baseline for the chart itself.
**Risk:** Medium-High. First chart in the app. Decision on the chart library has long-term implications (every future visualisation builds on it).
**Prerequisite:** Steps 1–5 done.

> Blok 2 of the daily flow. A swipeable / tabbed view that shows the 30-day or 90-day line chart, the streak counter, and tap-to-inspect bottom-sheet for any day. AC11–AC16 from the feature README.

---

## Acceptance criteria

- [ ] AC1: A horizontal swipe (or top-tab tap) on the home screen reveals the timeline. The two views (`Today` / `Tijdlijn`) are siblings, not separate routes — preserves SPA feel.
- [ ] AC2: The chart shows the last 30 days by default. A toggle (`30 / 90`) switches range. The 90-day range fetches lazily on first reveal.
- [ ] AC3: x-axis: dates (day numbers or weekday letters; readable on phone). y-axis: 1–10. Single line through the score points.
- [ ] AC4: Missing days render as a gap (a break in the line), not interpolated. Honest data.
- [ ] AC5: Streak counter above the chart: "X dagen achter elkaar". Counts back from today (or yesterday if today is unlogged) until the first gap.
- [ ] AC6: Tap a chart point → bottom sheet shows that day's full entry (score, note, tags). Tap outside / swipe down dismisses.
- [ ] AC7: Performance: 30-day view renders ≤ 200ms on a mid-tier phone; 90-day ≤ 400ms. No client-side filtering of a larger payload — the server endpoint returns exactly the range requested.
- [ ] AC8: Chart accommodates the historical dataset (1,363 days) — visually verified by switching to a custom 365-day range during dev (not exposed in UI; for the implementer's sanity check).

## Technical constraints

- **Chart library decision in this step.** Three candidates evaluated:

| Lib | Bundle | Pros | Cons | ADR? |
|---|---|---|---|---|
| Vanilla SVG (no dep) | 0 | No supply-chain surface; simple; total control | Manual axis/tick/tooltip work | No |
| uPlot | ~40 kB | Smallest mature lib; fast | Plain JS, not React; needs wrapper component | Yes |
| Recharts | ~80 kB | React-native, lots of docs | Larger bundle; harder to tree-shake | Yes |

**Default recommendation: vanilla SVG.** 30-90 points on a 1–10 scale is small; the manual work is ~80 LOC for the path + axes + tooltip and avoids a supply-chain surface that will need an ADR. If during implementation the SVG path math + tap-hit-test becomes hairy, fall back to uPlot with an ADR.

- Range data fetched via Step 1's `/api/day-entries?from=...&to=...`. No new endpoint.
- The swipe + tab UX uses CSS scroll-snap (no JS gesture library). Two `<section>` blocks horizontally adjacent; container has `scroll-snap-type: x mandatory`.
- Streak math: pure function in [`src/lib/domain/streak.ts`](../../../src/lib/domain/streak.ts) (new). Input: `DayEntry[]` + today's date. Output: `number`. Tested independently.

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01–A08 | No | Reuses Step 1's range endpoint |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | No | Read-only view of existing data |
| New dependency | ADR or step rationale | Maybe | If uPlot/Recharts chosen, ADR required. Vanilla SVG default → no ADR |
| `dangerouslySetInnerHTML` usage | A03 | No | SVG is just elements, no innerHTML smuggling |
| New env var with a secret | A02, A05 | No | — |
| New telemetry / observability dep | Cardinal "no telemetry" | No | — |

## Plan

### 6.1 New domain helper: `src/lib/domain/streak.ts`

```ts
export function currentStreak(entries: DayEntry[], today: string): number {
  // Sort by date desc, walk back from today (or yesterday if today missing),
  // count consecutive days; stop at first gap.
}
```

Heavy testing — easy to get edge cases wrong (year boundaries, today-is-logged-vs-not).

### 6.2 New component: `src/components/timeline-view.tsx`

Client component. Props: `initialEntries: DayEntry[]` (30-day from server), `today: string`. State: `range: 30 | 90`, `entries`, `selectedDate: string | null`. Fetches 90-day on first toggle.

### 6.3 New component: `src/components/score-chart.tsx`

Pure SVG. Props: `entries: DayEntry[]`, `range: 30 | 90`, `onPointTap: (date) => void`. ~80 LOC including axes + ticks + tap hit-test.

### 6.4 Update `src/components/today-shell.tsx`

Wraps the existing today view + new `<TimelineView>` in a horizontal scroll-snap container. Two tabs at top: `Vandaag` / `Tijdlijn`. Both views are server-side-rendered with their initial data.

### 6.5 Update server component `src/app/page.tsx`

Additionally fetches the last 30 days via Step 1's range endpoint and passes to `TimelineView` as `initialEntries`.

### 6.6 New bottom sheet: `src/components/day-detail-sheet.tsx`

When a chart point is tapped, opens with the day's score + note + tags. Reuses the empty-state copy from Step 5. Closes on background tap / Escape.

## Test plan

### `src/lib/domain/__tests__/streak.test.ts` (new, ~7 cases)

| # | Case |
|---|---|
| 1 | Today logged + yesterday logged + day before → streak 3 |
| 2 | Today missing + yesterday logged + day before → streak 2 |
| 3 | Today logged + yesterday missing → streak 1 |
| 4 | No entries → streak 0 |
| 5 | Entries with gaps further back don't extend streak |
| 6 | Year boundary (Dec 31 → Jan 1) handled correctly |
| 7 | Empty array → streak 0 |

### `src/components/__tests__/score-chart.test.tsx` (new, jsdom, ~4 cases)

| # | Case |
|---|---|
| 1 | Renders one `<path>` per gap-bounded segment |
| 2 | Renders one `<circle>` per data point |
| 3 | Tapping a point fires `onPointTap` with the right date |
| 4 | 30-day range renders ≤ 30 points; 90-day renders ≤ 90 |

### `src/components/__tests__/timeline-view.test.tsx` (new, jsdom, ~4 cases)

| # | Case |
|---|---|
| 1 | Renders streak counter + chart with initial 30-day data |
| 2 | Toggling to 90 fires a fetch and replaces entries |
| 3 | Tapping a point opens the bottom sheet |
| 4 | Bottom sheet shows the day's note + tags |

### `tests/e2e/daily-entry-timeline.spec.ts` (new, ~3 cases)

| # | Case |
|---|---|
| 1 | Swipe from Today → Timeline; streak counter visible |
| 2 | Toggle 30 → 90 → second fetch lands; chart updates |
| 3 | Tap a chart point → bottom sheet visible with the right day's content |

### Visual baseline

- One screenshot of the 30-day chart with realistic data, captured manually and saved as `docs/features/daily-entry/assets/timeline-30d-baseline.png` (gitignored if too large; in-doc thumbnail otherwise).
- Compared visually during refactor passes. Not asserted in Playwright (visual regression is overkill for a single-user app at v1).

## Done criteria

- [ ] `currentStreak` helper shipped + 7 unit tests green
- [ ] `score-chart.tsx` + `timeline-view.tsx` + `day-detail-sheet.tsx` shipped + 8 component tests green
- [ ] Playwright e2e +3 green
- [ ] Vitest count delta: +15 (7 streak + 4 chart + 4 timeline)
- [ ] Chart library decision recorded: defaulted to vanilla SVG. If `uPlot` or `Recharts` chosen, ADR at `docs/decisions/0005-chart-library.md` lands first.
- [ ] Visual baseline screenshot captured
- [ ] Manual: stopwatch the "open app → swipe to timeline → see streak" flow ≤ 2s on phone
- [ ] `npm run verify` clean

## Decision: defer or include?

Two items the feature plan deliberately deferred but the timeline tempts adding:

- **Tag correlation view** — "tagging X correlates with score Y". The `tag_correlations` Postgres view already exists in `directus/scripts/views/`. Adding a "common tags on good vs. bad days" panel here would be high-value. **Decision**: deferred. v1 ships the chart + streak; correlations are a follow-up.
- **Mobile install prompt** — "Add to home screen". Not implemented yet. **Decision**: deferred to a `pwa-install` feature later.
