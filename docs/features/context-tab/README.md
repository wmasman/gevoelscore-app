# Context tab — old vision doc (superseded)

**Status:** This folder's CONTENT is superseded by [features/verloop-and-episodes/](../verloop-and-episodes/). The original "Context tab" *vision* lived here; the active feature plan lives there.

**Note (2026-06-02 evening update):** The tab name "Context" was eventually **restored** as the final user-facing label after a three-pass naming exercise the same day (Verloop → Periodes → Context). What stayed retired is the original *data model* in this folder's older drafts — the Occurrence-type proposal got dropped, since tags-with-`parent_episode_id` ARE the occurrences. The active feature folder is still `features/verloop-and-episodes/` (folder slug preserved for git-history continuity); the user-facing tab label and the section structure described there match what this old vision doc originally proposed.

---

## Why this folder still exists

The v1.5 brainstorm session on 2026-06-02 resolved every open question this README originally listed:

- **Naming**: the tab is **Context** (final, 2026-06-02 evening — back to this folder's original name after the same-day Verloop → Periodes → Context cycle). Inside the Context tab, "Periodes" is a section heading. See [verloop-and-episodes/README.md §Naming](../verloop-and-episodes/README.md#naming).
- **Tag-vs-Episode boundary**: a clear decision rule was settled — `duration ≤ 1 day → tag; ≥ 2 days → episode`. The `gebeurtenis` and `interventie` tag categories survive. See [verloop-and-episodes/README.md §The conceptual model](../verloop-and-episodes/README.md#the-conceptual-model-resolved-2026-06-02).
- **Data shape**: a single polymorphic Episode collection with `category ∈ {interventie, levensgebeurtenis}`. `project` and `patroon` deferred to v2. The earlier "separate Occurrence type" proposal was dropped — **a tag with `parent_episode_id` set IS the occurrence**. See [verloop-and-episodes/README.md §Data model](../verloop-and-episodes/README.md#data-model).
- **Calendar binding UX**: deferred to v1.6. v1.5 ships manual-entry-only.
- **Timeline visualisation**: moved into its own feature, [features/timeline-episode-overlay/](../timeline-episode-overlay/), to ship after the Context tab + Episodes lands.

This folder is preserved as a redirect so anyone following an old link or a memory reference like `[[project-events-interventions-vision]]` lands somewhere readable.

## Where to go

- For the resolved feature plan → [features/verloop-and-episodes/](../verloop-and-episodes/)
- For the timeline overlay piece → [features/timeline-episode-overlay/](../timeline-episode-overlay/)
- For the architectural decision → [decisions/0006-three-surface-architecture.md](../../decisions/0006-three-surface-architecture.md)
- For the v1.5 roadmap → [roadmap.md](../../roadmap.md)
