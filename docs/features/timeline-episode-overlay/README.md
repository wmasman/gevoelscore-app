# Timeline episode overlay

**Feature:** Render Episodes as horizontal bands underneath the score line on the Tijdlijn (line-chart) and as background tints on the Heatmap. Tags that link to an episode (via `parent_episode_id`) appear as dots on their parent's band. The score signal stays the primary visual; episodes are context, not foreground.
**Version:** v1.5 (third feature to ship after `tag-recency-sort` and `verloop-and-episodes`)
**Status:** **Shipped 2026-06-02** — all 22 step-1 ACs ticked; verify gate green (1060 vitest); deploy + iOS soak pending.
**Parent docs:** [ADR 0006](../../decisions/0006-three-surface-architecture.md) (three-surface architecture — this feature is the "synthesis" half) · [features/verloop-and-episodes/](../verloop-and-episodes/) (data model + management UI) · [features/timeline-gap-indicator/](../timeline-gap-indicator/) (sibling timeline addition that already shipped)

---

## Overview

- **What:** Layer Episodes onto the existing Tijdlijn so the user can see, at a glance, what was going on during a score swing — "ah, that bad week was during the citalopram afbouw" or "the good week aligns with the holiday in week 28". Two views:
  - **Line chart**: episodes render as semi-transparent horizontal bands underneath the score line, spanning their date range. Linked tags (occurrences) render as dots on the band at their date.
  - **Heatmap**: episodes render as a soft background tint on each day-cell within their range, with a thin coloured edge on the cell's left to differentiate from the score-intensity tint.
- **Why:** A score line alone is one signal. Overlaying the things that were happening turns the timeline from "diary of feelings" into "diagnostic surface" — patterns the user can act on. This is the second-half deliverable of [ADR 0006](../../decisions/0006-three-surface-architecture.md); the Context tab (Periodes section) is "manage the episodes", Tijdlijn-overlay is "see them in context".

## Acceptance criteria

1. **Line chart — episode bands**:
   - Each non-archived episode whose [start_date, end_date] overlaps the visible chart range [from, to] renders as a horizontal rectangle below the score line area.
   - Rectangle y position is in a dedicated band-strip BELOW the chart's score plot area (NOT overlapping the score line). Reserve ~30px below the existing chart area for bands. Multiple concurrent episodes stack vertically (max 3 visible; overflow → "+N more" affordance, see Open questions).
   - Rectangle x position spans from `xFor(max(start_date, from))` to `xFor(min(end_date ?? to, to))`.
   - Rectangle colour comes from the episode's category: `interventie` = warm-earth accent at 30% opacity; `levensgebeurtenis` = neutral gray-tint at 25%. Tints picked to stay subordinate to the score line (per design brief restraint).
   - Rectangle is tappable: opens the episode's detail screen in the Context tab (cross-tab nav).
2. **Line chart — linked tag dots on band**:
   - For every tag attached to a day_entry where the tag has a `parent_episode_id` matching a visible band, render a small dot ON THE BAND at that day's x position.
   - Dot colour matches the band's category but at full opacity (1.0) so it reads against the band's 30% tint.
   - Dot is tappable: opens the QuickEntryFlow for that day (consistent with the existing raw-point and gap-dot behaviour — same `onPointTap(date)` callback).
3. **Heatmap — episode tint**:
   - Each day-cell that falls within a non-archived episode's range gets a left-edge coloured stripe (3px wide) using the episode category's colour. Stacked stripes (multiple concurrent episodes) are vertical bands inside the left-edge gutter.
   - The cell's main background tint (score intensity) stays primary; the edge stripe is the secondary signal.
   - No tap behaviour change — tapping a cell still opens QuickEntryFlow for that day. (Episode interaction lives on the line chart, not the heatmap.)
4. **Restraint principles**:
   - Score line (MA) stays the dominant visual. Bands sit BELOW the plot area, not behind it. The user's eye lands on the score first.
   - No animation. No motion. No tooltip-on-hover (we have aria-labels for SR users).
   - Reduced-motion `prefers-reduced-motion` already disabled animations globally; nothing to add.
5. **Accessibility**:
   - Each band has `role="button"`, `aria-label="{label} ({start_date} t/m {end_date}), tik om te openen"`.
   - Each linked-tag dot has `aria-label="{date}: {tag_label} (binnen {episode_label})"`.
6. **Both ranges supported**: 30d and 90d.
7. **Heatmap audit equivalence**: the heatmap's left-edge stripe pattern works in the same 7-column grid; doesn't push cell heights or widths.
8. **No regression**: existing score-line + MA + raw-point + gap-dot rendering on the line chart is unchanged when no episodes overlap the range. The score-only path test (already in [features/inline-tag-creation/](../inline-tag-creation/)) stays green.

## Technical constraints

- **No new dependency**. SVG additions to ScoreChart; CSS additions to ScoreHeatmap. Reuses the existing `xFor(date)` and `daysBetween(from, to)` helpers in ScoreChart.
- **Data source**: episodes are fetched alongside day_entries in the page-level server fetch. New prop `episodes: Episode[]` flows from `page.tsx` → `TodayShell` → `TimelineView` → `ScoreChart` + `ScoreHeatmap`. Same prop-driven re-render pattern as `initialEntries`.
- **Band-strip layout**: extend `SVG_HEIGHT` from 200 to ~230 to accommodate the band-strip below the existing plot area. OR reduce the existing PADDING_BOTTOM and use the freed space — depends on whether the x-axis labels still need their current room. Confirm in step file.
- **Performance**: with 90-day range and ~10 active episodes, this is ~900 day cells × ~10 episode-overlap checks = O(N) per render. Trivial. No memoisation needed beyond React defaults.
- **Stable band stacking order**: when multiple concurrent episodes overlap, stack by `start_date` asc (oldest at top of the band-strip). Deterministic — no z-fighting between renders.
- **Archived episodes**: NOT rendered on the timeline. Re-archiving an episode while the timeline is open should trigger a re-fetch via router.refresh (already in place).

## Test plan (sketch — to be detailed by `/plan-feature`)

- **Component test (ScoreChart)**: given an episode covering 2026-05-01 → 2026-05-10 and a chart range 2026-04-15 → 2026-05-15, a `<rect data-episode-id="X">` exists with x spanning the correct dates.
- **Component test**: tag with `parent_episode_id=X` on 2026-05-05 → a dot renders on episode X's band at the x for 2026-05-05.
- **Component test**: episode whose range is entirely OUTSIDE the chart range → no band rendered.
- **Component test**: 3+ concurrent episodes → first 3 stack vertically; 4th triggers "+1 more" affordance (defer if not in v1.5; see Open questions).
- **Component test (ScoreHeatmap)**: cell that falls within an episode range has the left-edge stripe (assertable via a `data-episodes` attribute on the cell or a child `<div class="episode-stripe">`).
- **Accessibility test**: band and dot have the documented aria-labels.
- **Regression**: existing "renders a tappable circle for each logged day" stays green; "gap-dot for missing days" stays green; "MA line" stays green.

## Out of scope (v1.5)

- **Editing an episode from the timeline**. Tapping a band navigates to the Context tab's episode detail; doesn't edit in place.
- **Multi-episode overlap visualisation beyond 3 stacks** (the "+N more" overflow UX). If real data shows >3 concurrent episodes is common, design properly in v1.6.
- **Garmin / continuous-stream layer**. Mentioned in the original ADR 0006 as a v2 background-layer concept. Not in v1.5.
- **Episode category colour customisation**. Two fixed colours (warm-earth for interventie, neutral for levensgebeurtenis). Per-user palette is v2.
- **Hover tooltips on bands** (showing description, dates, etc.). Tap-to-open-detail is enough for mobile. Desktop will need this eventually but Vandaag is mobile-first.

## Open questions

- **Band strip height**: 30px below plot area? Test on iPhone where chart is `h-48`. Might need a shorter strip (20px) at 90d when bands get tiny.
- **Overflow stacking**: how to handle >3 concurrent episodes. Possible: a stacked "..." indicator, or wrap below into a second mini-row. Defer the visual to step-file design; for now, document the cap.
- **Episode → tap → Context tab nav**: needs a route-level coordination so the Context tab opens to the right episode's detail. Possibly query-param `?episode=<id>`. Confirm shape in `/plan-feature`.
- **Heatmap left-stripe vs. corner-mark**: 3px left stripe might be too subtle. Alternative: a 4px-radius dot in the cell's top-left corner per episode. Sketch both before committing.
