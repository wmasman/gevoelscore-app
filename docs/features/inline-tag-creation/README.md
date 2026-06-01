# Inline tag creation

**Feature:** A `+ nieuw` chip at the end of each expanded category's chip row in the daily tag picker. Tapping it reveals an inline label entry + save button. Saving creates a tag in that category and auto-attaches it to today's entry.
**Version:** v1
**Status:** Planning — ready for `/plan-feature` to produce step file(s).
**Parent docs:** [REQUIREMENTS.md](../../REQUIREMENTS.md) · [design/brief.md](../../design/brief.md) · [features/tag/](../tag/) (Tag domain) · [features/tag-intelligence/](../tag-intelligence/) (vision — north star for tagging UX)

---

## Overview

- **What:** Replace the dead-end "Geen tags hier nog" empty-state and the missing add-affordance in [src/components/tag-category-list.tsx](../../../src/components/tag-category-list.tsx) with an inline create UX. Each expanded category gets a `+ nieuw` chip at the end of its chip row; tapping reveals an inline label field; saving creates the tag (category inherited from the section) and auto-selects it for today.
- **Why:** Currently there is no path to create a new tag from inside the daily flow. The user has to drop out to the admin UI or another tool to add a fresh tag — that breaks the cardinal principle (sub-10-second flow) and is hostile to brainfog users. The chip-style affordance keeps creation in-flow.

## Acceptance criteria

1. **Score-only path is unaffected.** A user who taps a score and dismisses the popout takes exactly the same number of taps as before this feature shipped. Verified by an integration test that drives the score → close path and asserts the timing/tap-count budget.
2. **Within the tag step, friction is reduced** (the north star — see [features/tag-intelligence/](../tag-intelligence/)). At minimum: the empty-state for a category becomes the create field rather than a dead-end message. Future iterations may add recent-first ordering, but that is *not* a hard requirement for this feature.
3. **Each expanded category** (including the 4 extra-options categories `gebeurtenis`, `interventie`, `project`, `custom`) shows a `+ nieuw` chip at the end of its chip row. The chip is visually distinct (outline-only, plus icon) but the same size/shape as existing chips so the row reads as continuous.
4. **Category is inherited from the section.** No category-picker in the create UX. A `+ nieuw` chip inside the `interventie` section creates an `interventie` tag.
5. **Save UX:**
   - Tapping `+ nieuw` reveals an inline text field with a label placeholder, Save button labelled **`Toevoegen`** (decided 2026-06-01), and Cancel affordance.
   - Enter key submits, Escape cancels, tapping outside the field cancels.
   - On save, the new tag is created server-side AND auto-selected for today's entry (added to the `day_entries_tags` join) in a single round trip from the client's perspective.
   - **Offline / network failure:** show a save-error on the existing save-status channel and let the user retry. No local queue, no optimistic-then-revert. Matches existing tag-select behaviour and the online-first posture of [ADR 0002](../../decisions/0002-pwa-with-directus-backend.md). Decided 2026-06-01.
6. **Server-side dedup.** Matching is case-insensitive on the *trimmed* label, *within the same category only*. Rules (all decided 2026-06-01):
   - **Whitespace:** trim leading/trailing whitespace before comparing. `" Pacing "` matches `"Pacing"`. Consistent with the trim-on-validate rule in the [Tag domain](../tag/).
   - **Cross-category:** does NOT match across categories. `paracetamol` in `interventie` and `paracetamol` in `custom` are distinct tags. Different category = different concept.
   - **Match found (active tag):** return the existing tag's id; the auto-selection then attaches that existing tag. Optional micro-feedback: a tiny "bestaat al, geselecteerd" hint.
   - **Match found (archived tag):** reactivate it — set `archived_at = null` server-side and return the existing id. Avoids leaving zombie rows when the user re-introduces a concept they previously archived.
   - **No match:** create the tag in the requested category and return its id.
7. **API route shape.** A new `POST /api/tags` route on the Next.js frontend takes `{ label, category }`, authenticates via the user's session cookie (not the scoped `frontend_sessions` Directus token — that role does not have CRUD on `tags`), forwards to Directus with the user's identity, returns `{ id, label, category, archived_at }`. The dedup logic lives in this route, not in the client.
8. **Empty-category state is replaced** by the create field itself. No more "Geen tags hier nog" copy. (Copy can be removed from [src/copy.ts](../../../src/copy.ts) when it's no longer referenced.)
9. **A11y:** the `+ nieuw` chip has an accessible label (e.g. `aria-label="Voeg tag toe aan {category}"`); the inline input has `aria-label="Nieuwe tag"`; the Save button has visible text; focus moves into the input on chip click and back to the new chip on save.
10. **Disabled gate respected.** When the daily flow's `editable` is false (no score committed yet), the `+ nieuw` chip is also disabled.

## Technical constraints

- **Schema is unchanged.** No `user_owner` is added to `tags` in this feature — see [features/tag-intelligence/](../tag-intelligence/) for the multi-user direction. New tags created in this feature get implicitly owned by Willem (the only current user); the future multi-user migration is a backfill, not a refactor of this code path.
- **Tag domain validation is reused AND extended.** Label rules come from [features/tag/](../tag/) — `validateTagLabel` is extended in this step (see step-1, sub-step 1.0) to add a **2-word maximum** (`MAX_TAG_LABEL_WORDS = 2`) and a 40-character sanity bound (`MAX_TAG_LABEL_LENGTH = 40`). Both new caps are inherited by the existing tag composer. Rationale for 2 words: matches the seeded tag vocabulary (single nouns or noun-phrases like "fysiotherapie", "minder slapen") and keeps chips compact at phone widths.
- **Status reporting.** The save uses the existing `useReportSaveStatus('tags', …)` channel so the consolidated header status reflects the create + select round-trip.
- **Optimistic UI** for the chip selection (new tag appears selected immediately, syncs server-side); revert on server error using the existing `lastSavedRef` snapshot pattern in `TagCategoryList`.

## Test plan (sketch — to be detailed by `/plan-feature`)

- **Component test (Vitest + Testing Library):** click `+ nieuw` reveals input; Enter submits; new tag appears selected; cancel closes without creating.
- **Component test:** existing tag chip remains intact and selectable after creation.
- **Hook/route test:** POST `/api/tags` happy path, plus the four dedup branches from AC #6:
  - case-insensitive existing label returns existing id, no duplicate created;
  - whitespace-padded label still matches the existing trimmed tag;
  - same label in a *different* category creates a new tag (NOT deduped);
  - matching an archived tag reactivates it (returns its id, `archived_at` cleared).
  - Plus error paths: unauthenticated returns 401, invalid label (empty / too long) returns 400.
- **A11y test:** axe scan of expanded category with `+ nieuw` chip + open input; focus management asserted.
- **Integration test:** score-only path tap-count regression test (acceptance #1).

## Out of scope (deferred to [features/tag-intelligence/](../tag-intelligence/))

- Recent-tags-first ordering.
- Inferring tags from notes.
- Surfacing algorithm based on relevance / time-of-day / score correlation.
- Merge / rename / consolidate UX.
- Per-user `user_owner` column on `tags`.

## Open questions

_All resolved 2026-06-01 — see "Save UX" acceptance criterion above. Save button is `Toevoegen`; offline behaviour is show-error-and-retry per [ADR 0002](../../decisions/0002-pwa-with-directus-backend.md)._
