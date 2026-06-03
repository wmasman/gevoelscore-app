# Tag management in Settings

**Feature:** A new "Tag-beheer" section on the `/settings` page that lets the user clean up their tag corpus — rename, recategorize, archive, un-archive, re-parent (set/clear `parent_episode_id` from the tag side), and hard-delete unused (usage_count === 0) tags. Drill-down per tag via a BottomSheet, mirroring the `EpisodeFormSheet` pattern. Surfaces archived tags behind a "Toon gearchiveerd" toggle. **No daily-flow regression** — the inline-create + recency-sorted picker in `QuickEntryFlow` stays untouched.
**Version:** v1.5b (administrative cleanup pass; ships after the v1.5 anchor + timeline overlay + today-card region all stabilised)
**Status:** **Shipped 2026-06-03** — all 22 ACs ticked; verify gate green (1148 vitest); deploy + smoke pending.
**Parent docs:** [REQUIREMENTS.md](../../REQUIREMENTS.md) · [features/verloop-and-episodes/](../verloop-and-episodes/) (step-5 deferred the tag-side re-parent path here) · [features/tag-recency-sort/](../tag-recency-sort/) (shipped sibling — same picker that benefits from cleanup) · [features/inline-tag-creation/](../inline-tag-creation/) (shipped sibling that creates the tag-corpus pressure this feature relieves)

---

## When does the user open Settings → Tag-beheer?

This is the question that scopes the feature. The daily flow never sends them here; daily flow has inline-create + the picker. They open Tag-beheer when:

- The tag list is **starting to feel cluttered** (~100+ tags with duplicates like `hoofdpijn` + `hoofdpijn licht` + `lichte hoofdpijn`)
- They created a tag in the **wrong category** and the picker keeps surfacing it wrong
- They want to **clean up** dead one-off tags from months ago
- An episode landed, and they want to **link existing tags** to it from the tag side (mirror of v1.5 episode-side picker)
- A tag's **spelling is wrong** and they want to rename it

If none of those hit, they never come here. The design pressure is "occasional cleanup pass", not "comprehensive admin". Different bar — less ambitious surface, more reliability where it counts.

## Actions in MVP

Ordered by guessed frequency-of-use, all live in the tag-detail BottomSheet that opens on tap:

1. **Rename** — fix typos / consolidate names. Label-cascade via tag-id reference (same as the existing rename-an-episode pattern). Low-risk.
2. **Recategorize** — move a wrong-category tag to its right category. Validation: target must be one of the 8 `TAG_CATEGORIES`.
3. **Archive (soft-delete)** — sets `archived_at`. Tag disappears from the daily picker but the history (every `day_entries.tag_ids[]` that references it) stays intact.
4. **Un-archive** — clears `archived_at`. Currently only possible via Directus admin; this fixes that gap.
5. **Re-parent / unlink** — set or clear `parent_episode_id` via a simple `behoort bij` dropdown (`Geen` + the list of non-archived episodes). Tag-side mirror of step-5's episode-side picker.
6. **Hard-delete** — only enabled when `usage_count === 0`. Confirmation dialog required (Settings is outside the no-friction rule). Atomic: removes the tag row entirely. Used to clean truly-dead clutter without leaving an archived row in the DB.

## Out of scope (v1.5b — defer to v1.5c)

- **Merge** (combine two tags into one, rewriting every `day_entries.tag_ids[]` reference to the source). Highest-value cleanup action; biggest implementation cost (atomic transaction across tags + day_entries). Defer until real usage shows which duplicates the user actually wants to merge.
- **Bulk select-mode** (multi-select recategorize / archive). Adds significant UI weight; only earns its keep after real per-item usage proves it's painful.
- **Search / filter by substring**. The grouped + recency-sorted list is scannable at 100 tags. Add search if real usage shows the list grows past ~200 OR the user reports scanning friction.
- **Per-tag usage stats UI** (`last used 2026-05-30, 23×`). The data is in the row but not rendered in the list — keeps the list shape clean (`label + category` only). Could surface inside the detail sheet later if useful.
- **Cross-category move via drag**. Tap-into-detail-screen handles it cleanly.

## UI shape

### Settings page placement

Three sections, in order:
1. Account (existing — logout)
2. **Tag-beheer** (new — the bulk of Settings traffic in practice)
3. Data (existing — binnenkort: export, delete)

Tag-beheer is the most-frequently-used Settings surface for a chronic-logging app, so it sits at the top of the "things you can act on now" cluster.

### List shape — A (label + category only)

The list renders one row per non-archived tag, grouped by category. Per-row content is intentionally lean — drill-down for detail.

```
[ Settings → Tag-beheer ]

  ☐ Toon gearchiveerd

  MENTAAL
    · pacing
    · helder hoofd
    · piekeren

  FYSIEK
    · hoofdpijn
    · vermoeid
    · misselijk

  INTERVENTIE
    · coaching sessie     · → Coaching met Sarah
    · paracetamol

  ...
```

- **Group order**: the canonical `TAG_CATEGORIES` enum order (mentaal / fysiek / overall / activiteit / gebeurtenis / interventie / project / custom).
- **Within category**: sort by **last-used desc** — surfaces actively-used tags at top, dead clutter sinks to bottom. Tags never used drop to the very bottom of their category (no last-used record → date sentinel '0000-00-00').
- **Linked-episode indicator**: each linked tag (parent_episode_id !== null) shows a small right-aligned `→ <episode label>` suffix on the row. Cheap visual signal that the link exists; the detail sheet handles editing it.
- **Archived toggle**: a single checkbox at the top — `Toon gearchiveerd`. When ON, archived tags render in their category groups with reduced opacity + a small `(gearchiveerd)` suffix.

### Tag-detail BottomSheet — `TagFormSheet`

Tap any row → opens a `TagFormSheet`, sibling component to `EpisodeFormSheet`:

Fields:
- **Naam** (rename input — text field, normalised on save)
- **Categorie** (dropdown / radio group of the 8 `TAG_CATEGORIES`)
- **Behoort bij** (dropdown: `Geen` + every non-archived episode label, ordered by start_date desc)
- **Status block**: `n keer gebruikt, laatst {dutch-date}` (read-only — gives the user grounding before they delete)

Action row at the bottom:
- **Bewaar** (primary — commits rename + recategorize + parent change in one PATCH)
- **Archiveer** OR **Activeer opnieuw** (toggles based on current archived_at state)
- **Verwijder** (hard-delete, only enabled when usage_count === 0; opens confirm)

### Hard-delete confirm

When the user taps **Verwijder** on a usage_count === 0 tag:

```
[ alertdialog inside the TagFormSheet ]

  Tag "{label}" definitief verwijderen?
  Deze actie kan niet ongedaan gemaakt worden.

  [ Annuleer ]  [ Ja, verwijder ]
```

Focus goes to `Annuleer` on appear (matches the logout-confirm pattern in [`settings-view.tsx`](../../../src/components/settings-view.tsx)). Enter from a brainfog user must NOT delete.

## Data model — no schema changes

Everything works on the existing `tags` collection. The fields exist already:
- `label` (rename)
- `category` (recategorize)
- `parent_episode_id` (re-parent / unlink)
- `archived_at` (archive / un-archive)
- `usage_count` (gates hard-delete)

The only new wire surface needed:
- **DELETE `/api/tags/[id]`** — hard-delete route, gated by usage_count === 0 (server-side check), 403 with `tag_in_use` error if positive.

Existing wire surface already supports the rest:
- POST `/api/tags` — exists (used by inline-create AND for the create-with-parent path from the episode side)
- PATCH `/api/tags/[id]` — exists from step-5; currently allows `parent_episode_id` only. **Needs extension** to also allow `label`, `category`, `archived_at` in the same patch. Allowed-key list grows from 1 → 4.

## Cross-feature integrity

- **No daily-flow regression**. `TagCategoryList` + `QuickEntryFlow` stay untouched. The inline-create chip still creates tags via POST `/api/tags`; the picker still sorts by recency-then-frequency-then-alphabetical.
- **Episode-side re-parent stays canonical for the creation path**. The Context-tab `TagPickerSheet` can create a new tag with parent pre-set in one round-trip; the Settings-side re-parent is for *existing* tags only (no inline-create here — that lives in the daily flow).
- **Renaming a tag propagates everywhere** because references are by id (same rule as episode rename). The display in the daily picker, the timeline linked-tag dots, the today-card linked-tag chips, and the export all pick up the new label automatically.
- **Hard-delete cascade**: usage_count === 0 means no `day_entries.tag_ids[]` reference exists. Directus has no FK from `day_entries.tag_ids` (it's a UUID array column), so the gate is logical (server-side check on the row's `usage_count`), not referential.

## References

- [features/verloop-and-episodes/](../verloop-and-episodes/) — step-5 deferred the tag-side re-parent path here.
- [features/tag-recency-sort/](../tag-recency-sort/) — shipped 2026-06-02; the picker benefits from a cleaner corpus.
- [features/inline-tag-creation/](../inline-tag-creation/) — shipped 2026-06-01; creates the corpus pressure this feature relieves.
- [roadmap.md](../../roadmap.md) — v1.5b slot.

## History

- 2026-06-03: feature folder created; brainstorm resolved 5 design decisions (merge defer; list shape A; hard-delete with confirm; tap-into-BottomSheet; dropdown for re-parent). Step file follows.
