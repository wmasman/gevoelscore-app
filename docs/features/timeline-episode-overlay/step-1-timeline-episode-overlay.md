# Step 1: Timeline episode overlay (single step)

**Estimated time:** ~6 hours. The largest single step in v1.5 — touches three components (`ScoreChart`, `ScoreHeatmap`, `TimelineView`), adds two pure-domain helpers, and integrates the existing `EpisodeFormSheet` into the timeline surface for in-place band edits.
**Test layers:** Vitest unit tests for the two new domain helpers (`computeEpisodeBandLayout`, `computeLinkedTagDots`). Vitest component tests for `ScoreChart` (band rendering, linked-tag dot rendering, dynamic SVG height) and `ScoreHeatmap` (left-edge stripe rendering). Vitest component tests for `TimelineView` (per-category toggle, in-place EpisodeFormSheet integration). Existing tests stay green. No new Playwright.
**Risk:** Medium-low. Pure-additive on the visual layer; no schema work, no API work, no auth work. Two real watch-points: (1) SVG layout dynamics — extending SVG_HEIGHT based on concurrent-episode count without breaking the existing y-axis math, and (2) cross-component prop threading (`episodes` already reaches TodayShell; need to forward to TimelineView).
**Prerequisite:** verloop-and-episodes step-5 shipped (commit `89e2378`+ `8c3cff3`). Episodes are persisted, tags can have `parent_episode_id`, and the `EpisodeFormSheet` component is ready to mount from a non-Context-tab parent.

> Step-1 ships the synthesis half of the v1.5 anchor. Episodes are surfaced as bands underneath the score line on the line chart and as left-edge stripes on the heatmap. Linked tags (tags with `parent_episode_id` set) render as dots ON their parent's band at the day they were logged. A per-category visibility toggle lets the user mute Interventies or Periodes independently. Tapping a band opens the same `EpisodeFormSheet` used in the Context tab, mounted in-place inside TimelineView — no cross-tab navigation.

---

## Resolved decisions (2026-06-02)

All four open questions from [README.md](README.md) settled:

- **Band-strip layout**: **extend SVG_HEIGHT from 200 to ~230+** (dynamic — see below). Bands sit BELOW the existing 200px plot area in their own strip. Score line + MA + raw points + gap dots stay in the upper 200px exactly as today; the bands are appended.
- **Overflow rule**: **no cap, dynamic strip height**. When more than 3 concurrent episodes overlap any day in the visible range, the strip grows to accommodate them. No silent dropouts; no "+N more" badge. Layout shift is bounded to episode mutations (which already trigger `router.refresh()` and re-render the chart), so it does not introduce *new* jitter.
- **Tap-to-edit nav**: **open `EpisodeFormSheet` in-place** inside TimelineView. Same component as the Context tab; no URL change, no tab-switch. The form's `tags` + `episodes` props get the same corpus TimelineView already has access to.
- **Heatmap mark**: **3px left-edge stripe** per overlapping episode, stacked horizontally inside the cell's left gutter when multiple episodes overlap a single day. The cell's score-intensity tint stays primary.
- **Visibility toggle**: **per-category (2 checkboxes)** — `Interventies` and `Periodes`. Both default to ON. State is local (useState in TimelineView), resets on reload. Toggle UI lives in the existing range/view-toggle bar.

---

## Acceptance criteria

### Domain layer

- [x] **AC1: `computeEpisodeBandLayout(episodes, from, to)` lives at `src/lib/domain/episode-band-layout.ts`**. Pure function. Input: full episode list + visible range. Output: array of band rows, where each row is `{ episode, rowIndex, xStartDate, xEndDate }`. Rules:
  - Skip archived episodes (already filtered upstream, but defensive).
  - Skip episodes whose range does NOT overlap `[from, to]`.
  - Sort by `start_date` ascending; stack into rows greedily — episode N goes in the first row where no existing band's `[xStartDate, xEndDate]` overlaps. Deterministic across renders.
  - `xStartDate` = `max(episode.start_date, from)`. `xEndDate` = `min(episode.end_date ?? to, to)`.
  - `rowIndex` is 0-based; the maximum rowIndex across all output bands determines the strip's total row count.
- [x] **AC2: `computeLinkedTagDots(entries, tags, episodes, from, to)` lives at `src/lib/domain/linked-tag-dots.ts`**. Pure function. Input: day_entries, full tag corpus, full episode corpus, visible range. Output: array of `{ date, episodeId, tagId, rowIndex }`. Rules:
  - For each entry in range, for each `tag_id` in `entry.tag_ids`, look up the tag.
  - Skip tags whose `parent_episode_id` is null OR whose parent isn't a visible band (archived parent, parent outside range, etc.).
  - The `rowIndex` is the rowIndex of the parent's band from `computeEpisodeBandLayout`. Same input deterministic.

### ScoreChart extensions

- [x] **AC3: ScoreChart accepts new props** `episodes: Episode[]`, `allTags: Tag[]`, `categoriesVisible: Record<EpisodeCategory, boolean>`, `onEpisodeTap: (episode: Episode) => void`. All optional with safe defaults to keep existing component tests passing.
- [x] **AC4: SVG height extends dynamically** based on band-row count. Base height stays 200px (the score-plot area). Below it, a band strip of `BAND_ROW_HEIGHT * rowCount` (where `BAND_ROW_HEIGHT = 8` and `rowCount` = `max(rowIndex) + 1` from the band layout, or 0 if no bands). Final SVG_HEIGHT = `200 + (rowCount > 0 ? BAND_STRIP_PADDING_TOP + BAND_ROW_HEIGHT * rowCount + BAND_STRIP_PADDING_BOTTOM : 0)`.
- [x] **AC5: Each visible band renders as a `<rect data-episode-id="{id}" data-episode-category="{cat}">`**. x position spans the visible date range; y is `200 + BAND_STRIP_PADDING_TOP + rowIndex * BAND_ROW_HEIGHT`; height is `BAND_ROW_HEIGHT - BAND_GAP` (≈6px visible band, 2px gap between rows).
- [x] **AC6: Band fill colour by category**: `interventie` → warm-earth accent at 30% opacity (CSS variable `--color-accent`). `levensgebeurtenis` → neutral surface-muted at 50% opacity. Tints subordinate to the score line, per design brief.
- [x] **AC7: Each band has `role="button"`, `tabIndex={0}`, and `aria-label="{label} ({startDutch} t/m {endDutch or 'lopend'}), tik om te bewerken"`.** Click + Enter + Space all invoke `onEpisodeTap(episode)`.
- [x] **AC8: Each linked-tag dot renders as a `<circle data-tag-id="{id}" data-episode-id="{parentId}">`** on its parent's band. x = `xFor(date)`, y = band's vertical centre, r = 3. Fill matches the parent band's category colour at 100% opacity. `aria-label="{dutchDate}: {tagLabel} (binnen {episodeLabel})"`. Click invokes the existing `onPointTap(date)` callback (consistent with other tap targets on the chart).
- [x] **AC9: Category filter applies BEFORE band layout**. If `categoriesVisible.interventie === false`, no `interventie` episodes contribute bands OR strip height. The layout helper accepts the filter as input OR the parent pre-filters before calling — pick the cleaner one in implementation.
- [x] **AC10: When ALL bands are filtered out OR no episodes overlap the range, SVG_HEIGHT collapses back to 200px**. No empty strip, no extra padding. The score plot is identical to the pre-step-1 chart.

### ScoreHeatmap extensions

- [x] **AC11: ScoreHeatmap accepts new props** `episodes: Episode[]`, `categoriesVisible: Record<EpisodeCategory, boolean>`. Both optional with safe defaults.
- [x] **AC12: Each day-cell that falls within a visible (non-filtered) episode's range renders left-edge stripes**: a 3px vertical band per overlapping episode, stacked left-to-right inside the cell's left gutter. Stripe colour = same category palette as the line-chart bands. The cell's existing score-intensity background tint is unchanged.
- [x] **AC13: Heatmap tap behaviour is UNCHANGED**. Tapping a cell still opens QuickEntryFlow for that day. The stripes are visual signals only; episode interaction lives on the line chart.

### TimelineView integration

- [x] **AC14: `TimelineView` accepts new props** `episodes: Episode[]` (required) and `tags: Tag[]` (required — renames the existing `allTags` prop OR uses it directly; pick the cheaper rename or pass-through).
- [x] **AC15: A new toggle row** appears in the existing range/view-toggle bar with two checkboxes: `Interventies` and `Periodes`. Both default to ON. State is `useState<Record<EpisodeCategory, boolean>>`. Clicking either toggles the category's visibility AND triggers a re-render of both ScoreChart and ScoreHeatmap.
- [x] **AC16: Tapping a band on the chart opens `EpisodeFormSheet` in-place** inside TimelineView. The form receives `mode='edit'`, `category=episode.category`, `initialEpisode=episode`, `tags={tags}`, `episodes={episodes}`, plus the same `onClose`/`onSaved`/`onArchived` closure pattern as ContextView. The sheet's open/close state is local to TimelineView.
- [x] **AC17: After save/archive, the sheet closes and the chart re-renders** with the fresh episode set (via the existing `router.refresh()` plumbing in `useEpisodeUpsert`). No client-state shadow.

### Prop threading

- [x] **AC18: `page.tsx` already fetches `episodes`** in the Promise.all and passes to TodayShell. TodayShell threads `episodes` through to TimelineView (currently does NOT — adds the prop).
- [x] **AC19: Heading hierarchy + a11y stay correct.** The chart's existing `aria-label` on the SVG region carries the score-line description; bands' per-button `aria-label`s describe each episode individually.

### Cross-feature integrity

- [x] **AC20: Daily-flow tag picker (`TagCategoryList` in QuickEntryFlow) is UNCHANGED**. No regression: tag-creation in Vandaag does NOT gain a band-related affordance.
- [x] **AC21: Existing chart tests stay green**: score line, MA, raw-point dots, gap dots, heatmap cells. The band/dot additions are purely append.
- [x] **AC22: Existing TimelineView tests stay green**: range toggle (30/90), view toggle (chart/heatmap), past-day-edit QuickEntryFlow. The new toggle row is *additive*.

---

## Technical constraints

- **No new dependency.** SVG `<rect>` and `<circle>` for the line chart; CSS / `<div>` for the heatmap stripes. Reuses ScoreChart's existing `xFor(date)` and `daysBetween(from, to)` helpers.
- **Pure-domain layout helpers**. `computeEpisodeBandLayout` + `computeLinkedTagDots` live in `src/lib/domain/`, take no React, no DOM, no time-of-day — fully testable in isolation. The chart component is thin: derive layout, render.
- **Dynamic SVG_HEIGHT** does not affect viewport size of the parent container (`<div>` with `h-48` etc.). The SVG itself stretches; the container scrolls if needed. Verify on iPhone widths that the bands at maximum row-count (e.g. 5+ concurrent episodes) don't push the past-day list visually off-screen.
- **Category filter scope**: filter ONLY the line chart + heatmap bands. The Context tab's list is unaffected; same for the Periodes section. Filter is local TimelineView state.
- **Band stacking determinism**: `computeEpisodeBandLayout` sorts by `start_date` asc, then ties broken by `id` lexicographic. Same input always produces the same band rows; no z-fighting across re-renders.
- **Linked-tag dot positioning**: dots sit at the vertical centre of their parent band. If the parent band is hidden (filtered out), the dots ARE NOT rendered. Verified by test.
- **No `useEffect` for layout**: band rows + dot positions are derived synchronously from the props on each render. No state. No async.
- **Episode bands at the right edge**: when `episode.end_date === null` (lopend), the band extends to `to` (the right edge of the chart). When the episode starts before `from`, it extends from `from`. Both are clamping operations in the helper.
- **Heatmap stripe layering**: 3px stripes stack horizontally in the cell's left edge (so 3 concurrent episodes = 9px of left gutter occupied). Verify at narrow iPhone widths that 9px doesn't visually crowd out the score-intensity tint's readable area.
- **TimelineView prop chain**: `page.tsx → TodayShell → TimelineView` for episodes. ScoreChart + ScoreHeatmap receive episodes + categoriesVisible from TimelineView.
- **Tap targets**: each band must satisfy WCAG 2.5.5 (44×44 effective tap target). At `BAND_ROW_HEIGHT=8` the band's *visual* height is ~6px, but its *hit* area should expand vertically. Use SVG `pointer-events` + an invisible wider `<rect>` overlay if needed, OR ensure the row-pitch is tall enough. Validate in iOS soak.

---

## Test plan

### Domain helpers

`src/lib/domain/__tests__/episode-band-layout.test.ts` (NEW)

1. Empty input → returns `[]`.
2. Single episode fully inside range → one row, rowIndex 0.
3. Single episode partially overlapping range (starts before `from`) → xStartDate clamped to `from`.
4. Single episode partially overlapping range (ends after `to` OR end_date null) → xEndDate clamped to `to`.
5. Episode entirely outside range → not included in output.
6. Archived episode → not included.
7. Two non-overlapping episodes → both in row 0.
8. Two overlapping episodes → first in row 0, second in row 1.
9. Three episodes A (1-10), B (5-15), C (8-20) → A in row 0, B in row 1, C in row 2 (greedy stacking).
10. Three episodes A (1-5), B (6-10), C (3-8) — A and B don't overlap, C overlaps both — A in row 0, B in row 0 (after A), C in row 1.
11. Deterministic ordering: same input twice → same output (run the function twice, deepEqual).
12. Tie-breaking by id: two episodes starting on the same day → ordered by id lexicographic.

`src/lib/domain/__tests__/linked-tag-dots.test.ts` (NEW)

13. No entries → returns `[]`.
14. Entry has tag whose parent_episode_id matches a visible band → one dot with the band's rowIndex.
15. Entry has tag whose parent_episode_id is null → no dot.
16. Entry has tag whose parent_episode_id points to an archived episode → no dot.
17. Entry has tag whose parent_episode_id points to an out-of-range episode → no dot.
18. Multiple tags on one day, each linked to a different visible episode → multiple dots.
19. Tag exists in corpus but isn't referenced by any entry in range → no dot.

### ScoreChart

`src/components/__tests__/score-chart.test.tsx` (EXTEND)

20. Default props (no episodes) → SVG_HEIGHT is 200; no `<rect data-episode-id>` rendered (regression).
21. One episode fully overlapping range → one `<rect data-episode-id="X">` rendered with the correct x span.
22. SVG_HEIGHT extends correctly when bands are present: 200 + padding + row-count * row-height.
23. Two concurrent episodes → 2 bands stacked, SVG_HEIGHT = 200 + padding * 2 + 2 * row-height.
24. Band has the documented `role="button"` + `aria-label`.
25. Clicking a band calls `onEpisodeTap(episode)`.
26. Keyboard: Enter on focused band → calls `onEpisodeTap`.
27. Linked-tag dot renders on the band at its date's xFor.
28. Dot has the documented `aria-label`.
29. Clicking the dot calls `onPointTap(date)` (same handler as raw-points + gap-dots).
30. categoriesVisible.interventie=false → all interventie bands AND their dots disappear.
31. All bands hidden via filter → SVG_HEIGHT collapses back to 200.
32. Episode with end_date=null → band extends to the chart's right edge.

### ScoreHeatmap

`src/components/__tests__/score-heatmap.test.tsx` (EXTEND)

33. Default props (no episodes) → no left-edge stripe elements (regression).
34. One episode covering 3 days in range → 3 day-cells each have a left-edge stripe element.
35. Two concurrent episodes in the same day → that day's cell has 2 stripe elements stacked left-to-right.
36. Stripe colour matches the line-chart category palette.
37. categoriesVisible.levensgebeurtenis=false → all levensgebeurtenis stripes disappear.
38. Cell tap behaviour is unchanged (existing test stays green).

### TimelineView

`src/components/__tests__/timeline-view.test.tsx` (EXTEND)

39. Renders the per-category toggle row with both checkboxes checked by default.
40. Unchecking "Interventies" calls re-render with `categoriesVisible.interventie === false`.
41. The two checkboxes are independent — unchecking one leaves the other on.
42. Toggle state resets to default ON when the component remounts.
43. Tapping a band in the chart opens the `EpisodeFormSheet` mounted by TimelineView, in edit mode, with the correct episode.
44. After saving the episode in the in-place sheet, the sheet closes; chart re-renders via router.refresh (mocked) with fresh data.
45. Closing the sheet via the close button restores focus to the band that opened it (light-touch verification — focus management contract).

### TodayShell wiring

`src/components/__tests__/today-shell.test.tsx` (EXTEND)

46. TodayShell forwards `episodes` to TimelineView when the user is on the Tijdlijn tab.

### Regression suite

47. Daily flow QuickEntryFlow tests stay green.
48. Existing context-view tests stay green.
49. Episode-form-sheet integration tests stay green (the form is reused but unmodified).
50. `npm run verify` is green at the end of every phase.

---

## Build order (TDD shape — RED → GREEN → REFACTOR per phase)

Six phases. Each phase is its own RED-first cycle. Verify gate green at each phase boundary.

1. **Domain helpers**: `computeEpisodeBandLayout` (tests 1–12) + `computeLinkedTagDots` (tests 13–19). Pure functions, fastest feedback loop. RED, implement, GREEN.
2. **ScoreChart bands**: tests 20–32. Extend props, render bands + dots, dynamic SVG_HEIGHT. RED, implement, GREEN.
3. **ScoreHeatmap stripes**: tests 33–38. Extend props, render left-edge stripes. RED, implement, GREEN.
4. **TimelineView toggle + integration**: tests 39–45. Add toggle row, in-place EpisodeFormSheet wiring. RED, implement, GREEN.
5. **TodayShell wiring**: test 46. Thread episodes prop to TimelineView. RED (small), implement, GREEN.
6. **Verify gate + iOS soak prep**: run the full `npm run verify`, manual smoke-on-prod by tapping a band, verify the FormSheet opens correctly. Commit + push + deploy.

Commit at each phase boundary. The verify gate must be green before moving to the next phase.

---

## Out of scope (v1.5)

- **Garmin / continuous-stream background layer**. ADR 0006 mentions this as a v2 concept. Not in v1.5.
- **Per-user colour customisation** for category palettes. Two fixed colours; v2.
- **Hover tooltips** on bands (showing description, dose, etc.). Tap-to-open-form is enough on mobile. Desktop can revisit when there's a real desktop use-case.
- **Episode-edit-from-heatmap**. The heatmap's tap behaviour stays score-only. Episode editing happens on the chart band, not the heatmap cell.
- **Per-episode visibility toggle** (granular hide of one specific episode). Per-category is the v1.5 shape; per-episode is v1.6+ if real data shows it's needed.
- **Deep-linking via `?episode=<id>`** query param. The in-place EpisodeFormSheet decision removed the need.

---

## Notes for the next feature

What the next feature ([tag-management-settings/](../tag-management-settings/), v1.5b) needs to remember from step-1:

- The Tijdlijn now hosts `EpisodeFormSheet` in-place. If tag-management-settings adds an analogous tag-detail surface, the same in-place pattern is available — no need to design cross-tab navigation either.
- Linked-tag dots on the timeline are the strongest visual signal that tags-with-parents work. Settings → Tag-beheer's "behoort bij" picker should be careful NOT to break this visual chain (don't allow re-parenting in a way that confuses the timeline derivation).
- The `categoriesVisible` toggle is a local-state pattern; if tag-management-settings adds analogous filters (e.g. archived-tag visibility), use the same shape — local state, defaults to "show what matters", no persistence.
