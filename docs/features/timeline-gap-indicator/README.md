# Timeline gap indicator

**Feature:** A restrained visual cue on the timeline for days that have no score (skipped or future-not-yet-logged days). No copy, no guilt-trip language; a faint hollow dot at the score position is the canonical shape.
**Version:** v1
**Status:** Planning — ready for `/plan-feature` to produce step file(s).
**Parent docs:** [REQUIREMENTS.md](../../REQUIREMENTS.md) · [design/brief.md](../../design/brief.md) (forbidden patterns: no guilt-tripping cues)

---

## Overview

- **What:** Render every day in the active timeline range, including days without a `day_entry`. Score-less days appear as a faint hollow dot (low-opacity outline-only circle) at a neutral vertical position; scored days continue to render exactly as today.
- **Why:** A 100%-coverage user (1.363 days, see [brief](../../app_brief_gevoelscore.md)) wants the timeline to honestly reflect *which* days were logged. Currently absent days are silently skipped — visually indistinguishable from "no data range" — and the user can't see at a glance where the gap is. The brief and the design tone are explicit that the cue must be quiet (no `Gemist`, `Geen score`, alarming red, exclamation marks): the goal is gap-awareness, not nudging.

## Acceptance criteria

1. **Every calendar day in the active timeline range is rendered**, not just days with a `day_entry`. Score-less days appear as a faint hollow dot.
2. **The hollow dot is visually distinct from scored dots** but quiet enough that it doesn't compete for attention: outline-only, lowered opacity, neutral colour from the design tokens (no warm-orange or alarm colour).
3. **No copy** accompanies the indicator. No `Geen score`, no `Gemist`, no tooltip on hover that introduces guilt-tripping language. Hover/focus may show a neutral date string only.
4. **Accessibility:** the dot has a non-visual label for assistive tech (e.g. `aria-label="2026-05-20, geen score"`) so screen-reader users get parity with sighted users. The visual treatment alone is *not* the only signal.
5. **The score-only path is unaffected.** No regression in the daily entry flow; this is purely a Tijdlijn-side rendering change.
6. **Honest representation of future days.** Future days in the current range are also score-less by definition; they get the same hollow dot. No special "upcoming" visual.

## Technical constraints

- **Data source.** The timeline already fetches a range of `day_entries`. The renderer needs to derive the full list of dates in the range (a date sequence between `range_start` and `range_end`) and left-join the fetched entries onto it. The join logic lives in the frontend, not in a new API endpoint.
- **Performance.** The 30/90 day views are small enough that derive-in-render is fine. The "all 1.363 days" view (if exposed) needs a virtualised list — out of scope for this feature unless that view is brought forward.
- **Design tokens.** Uses existing `--color-fg-subtle` (or a new lower-opacity variant if `--color-fg-subtle` is now used elsewhere — verify against [src/app/globals.css](../../../src/app/globals.css)).

## Test plan (sketch — to be detailed by `/plan-feature`)

- **Component test:** timeline with mixed scored + score-less days renders the right number of dots, with hollow dots in the right positions.
- **Component test:** future days (after `today`) in the visible range render as hollow.
- **A11y test:** axe scan asserts the aria-label pattern.
- **Visual baseline:** a screenshot regression for the timeline with at least one gap.

## Open questions

- **Default range.** Brief mentions 30 / 90 days. Does the gap indicator appear in both? (Assume yes; confirm in `/plan-feature`.)
- **Calendar view (future).** The brief mentions a possible calendar view in future versions. The hollow-dot pattern likely transfers to a calendar grid as a lighter cell tint. Document the parallel when the calendar view is scoped — not now.
- **"Strong" mode.** If the soak reveals that the faint hollow dot is too quiet to register, a stronger cue (dashed line at the score-zero position, slight background tint to the day column) is a fallback. Defer the decision to user feedback — do not pre-build both.
