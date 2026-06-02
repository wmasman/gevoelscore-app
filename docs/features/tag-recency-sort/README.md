# Tag recency sort within category

**Feature:** Within each expanded category in the daily tag picker, sort chips by recency-then-frequency-then-alphabetical instead of pure-alphabetical. The chip the user picked most recently and most often floats to the front of its category. No new UI; no LLM; no cross-category surfacing.
**Version:** v1.5a (first piece of v1.5 — ships independently before the bigger verloop-and-episodes feature)
**Status:** **Shipped 2026-06-02** (commit `426be73`). `computeRecencyByTagId` lives in [`src/lib/domain/tag-sort.ts`](../../../src/lib/domain/tag-sort.ts); wired into [`TagCategoryList`](../../../src/components/tag-category-list.tsx) and threaded through `TodayShell` + `TimelineView` so the within-category sort applies in both today's flow and past-day editing.
**Parent docs:** [REQUIREMENTS.md](../../REQUIREMENTS.md) · [features/tag-intelligence/](../tag-intelligence/) (parent vision — this is the v1.5 slice) · [features/inline-tag-creation/](../inline-tag-creation/) (the feature that introduced the inline `+ nieuw` chip)

---

## Overview

- **What:** Reorder the chips inside each expanded category in [`src/components/tag-category-list.tsx`](../../../src/components/tag-category-list.tsx). Current order is `sort: ['category', 'label']` (alphabetical, set in [`src/lib/api/tags.ts`](../../../src/lib/api/tags.ts) `readAllTags`). New order *within* each category: recency first (most recently used), then frequency (most used overall) as a tie-breaker, then alphabetical as a final tie-breaker.
- **Why:** The brainfog user reaches for the same handful of chips most days. Alphabetical sort forces them to scan every time. Recency-first surfacing makes the right chip the *first* chip — no scanning, no thinking. This is the v1.5-slice of the bigger tag-intelligence vision in [features/tag-intelligence/](../tag-intelligence/); the surfacing algorithm here is purely local (no LLM, no cost, no privacy concerns).

## Acceptance criteria

1. **Within each expanded category**, chips render in order: most-recently-attached first (across all `day_entries_tags` rows the user has), then by `usage_count` desc, then alphabetical asc.
2. **Category headers and order are unchanged.** The 4 primary categories + Extra-opties toggle + 4 extra categories all appear in the same positions as today. Only the chip order INSIDE each expanded category shifts.
3. **The recency signal is "last used" — the most recent `day_entries_tags.day` for that tag-id**, irrespective of the current date range visible in the picker. (If a tag was used 6 months ago and never since, it sinks below tags used last week.)
4. **Score-only path is unaffected** (per [features/tag-intelligence/](../tag-intelligence/) guiding principle). A user who taps a score and dismisses the popout without expanding a category does NOT trigger any new sort computation. The sort is computed lazily, only when a category is expanded.
5. **No new UI affordance.** No "recent" badge, no "voor jou" section, no separate strip. Just a reorder. Restrained per the design brief.
6. **Empty / new-user case**: if the user has no `day_entries_tags` history (or this is a fresh tag with usage_count=0), fall back to alphabetical. No tag is *hidden* by the sort; only reordered.
7. **Inline-tag-creation**: a newly created tag enters the category at the front of the list (it's the most-recently-used by definition). The existing scroll-into-view + focus behaviour stays.
8. **Heatmap and timeline views**: unaffected. The recency sort is only the daily-flow tag picker.
9. **Verify gate**: `npm run verify` clean.

## Technical constraints

- **Recency data source**: derive from the existing `day_entries_tags` join. The lib needs to expose `tag.last_used_at` (timestamp of the most recent attachment) per tag, alongside `usage_count` (already present). One small SQL/SDK aggregate query, OR computed client-side from the already-fetched day_entries history.
  - **Recommendation**: server-side aggregate via a Directus query (`?aggregate[max]=day_entries_tags.day&groupBy[]=tags.id`). Computing client-side requires shipping the full junction history to the browser, which scales poorly with 1.3k+ days.
  - Confirm shape in `/plan-feature`.
- **No new dependency**. Reuses the existing tag-fetch path in `readAllTags`. The aggregate is one extra query OR baked into the existing query.
- **Caching**: the sort recomputes on each tag-picker render. With ~83 tags the sort is trivial; no memoisation needed beyond what React already does.
- **No new schema column**. The existing `usage_count` column is preserved. `last_used_at` is derived, not stored — though a future v1.6 optimisation could materialise it as a column.
- **Privacy posture unchanged** — this feature is local-only, no external calls, no LLM. Matches the cardinal "no telemetry" principle.

## Test plan (sketch — to be detailed by `/plan-feature`)

- **Unit (domain)**: a sort comparator `compareTagsForPicker(a, b)` that takes two tags-with-recency and returns -1/0/1. Tests for: pure recency order, frequency tiebreaker, alphabetical tiebreaker, missing-recency fallback.
- **Unit (lib)**: extend `readAllTags` (or add a new sibling fn) to attach the `last_used_at` field per tag. Test the aggregate query shape against a mocked Directus.
- **Component**: extend `src/components/__tests__/tag-category-list.test.tsx` to assert that, given mixed-recency tags, the chip render order matches the expected sort. The "+ nieuw chip renders at end" test still passes (the + nieuw chip is the LAST chip rendered, unaffected by sort).
- **No e2e change needed** — visual behavior; verified manually on dev server.

## Out of scope

- Cross-category surfacing (no "recent strip" above the categories — that was an alternative considered in the brainstorm and rejected for being too prominent for a brainfog-sensitive surface).
- LLM-driven note → tag inference. v2. See [features/tag-intelligence/](../tag-intelligence/).
- Merge / consolidate / archive UX for tags. v1.5b — see future `features/tag-management-settings/`.
- Per-user surfacing models (training a recommender per user). v2.
- A "frequent / forgotten" inverse view ("here are tags you used to use a lot but haven't in 30 days"). Interesting but speculative.

## Open questions

- **Recency aggregate query**: does Directus support `aggregate[max]` on a junction field? Verify against [Directus filter/aggregate docs](https://github.com/directus/docs) before step-file write. If unsupported, fall back to client-side derivation from a `day_entries_tags` window read (e.g. last 90 days, 1 query).
- **"Recent" cutoff**: should tags un-used for > 6 months sink ALL THE WAY to the bottom (below alphabetical), or just be tie-broken alphabetically? Probably just tie-broken — keep the rule simple. Confirm in `/plan-feature`.
