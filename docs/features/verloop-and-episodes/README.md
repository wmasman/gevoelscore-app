# Context tab + Episodes

**Feature:** The v1.5 anchor. Adds a new third top-level surface (**Context**) that holds the contextual signals affecting daily scores over time. The first (and currently only) section inside Context is **Periodes** — multi-day Episodes for interventies (coaching, physio, ergo, medication courses) and levensgebeurtenissen (holidays, partner-away weekends, big work projects). Adds a new `episodes` Directus collection, a new nullable `tags.parent_episode_id` FK so single-day tags can hang off an ongoing episode as occurrences, and the Context-tab UI for episode CRUD + tag-linking. The Context container is named for the extensibility: v1.6 Calendar bindings and v2 project context become sibling sections under the same tab.
**Version:** v1.5
**Status:** Designed — brainstorm resolved 2026-06-02; tab label finalised 2026-06-02 after three same-day passes (Verloop → Periodes → **Context**). Step-1 through step-5 shipped (test-suite + verify-gate green). Deploy + iOS soak pending.
**Parent docs:** [ADR 0006](../../decisions/0006-three-surface-architecture.md) (three-surface architecture) · [REQUIREMENTS.md](../../REQUIREMENTS.md) · [design/brief.md](../../design/brief.md) · [features/tag/](../tag/) (Tag domain — referenced for the new `parent_episode_id` field)

> **Folder slug note**: this folder is `features/verloop-and-episodes/` for git-history continuity. The user-facing tab label is **Context**; Periodes is a section heading INSIDE that tab. Do not rename the folder; treat the slug as an internal identifier only.

---

## Naming

- Tab name: **Context** (Dutch, "context"). Final resolution 2026-06-02 after three same-day passes:
  1. Brainstorm: "Verloop" — rejected for the expiry/decay echo of "verloopdatum" and the clinical lean.
  2. Same-day revision: "Periodes" — rejected because the tab needed a container name large enough to also hold v1.6 Calendar bindings + v2 project context as sibling sections. "Periodes" describes only the date-range things.
  3. Same-day final: **Context** — the container abstraction. Periodes remains as a section heading inside.
- Tab order in the bottom nav: **Context / Vandaag / Tijdlijn**. Vandaag is **centre-positioned** so the daily-flow action is thumb-balanced on both right-hand and left-hand grip.
- Data type: **Episode** (English in code, "interventie" / "levensgebeurtenis" in user copy).
- Junction: a Tag's optional pointer to its parent episode is called `parent_episode_id`.

## Data model

### `episodes` collection (new)

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | PK |
| `label` | string | Trimmed (whitespace normalised), non-empty, **max 40 chars** (resolved 2026-06-02 — same ceiling as tag-label for scannability). **No word-count constraint** (unlike tag-label's 2-word rule) so natural 3-4 word episode names like "Coaching met Sarah" and "Wekelijkse fysio bij Marieke" pass. Narrative content (dose schedules, frequencies, practitioner details) belongs in `description`, not the label. |
| `category` | enum | `interventie` \| `levensgebeurtenis`. v1.5 enum is tight; `project` + `patroon` deferred to v2 (see "Out of scope") |
| `start_date` | DATE | ISO YYYY-MM-DD. **No constraint relative to today** — future-dated episodes allowed (resolved 2026-06-02; real case: book a vakantie 3 months out) |
| `end_date` | DATE \| null | null = ongoing. When set, must be `>= start_date` (validated by `validateDateRange`) |
| `description` | text \| null | Optional free-text notes for the episode |
| `calendar_binding` | JSON \| null | Reserved for v1.6 (Google Calendar series binding). Always null in v1.5. |
| `archived_at` | timestamp \| null | Soft-delete; episodes are never hard-deleted from the UI (preserves linked-tag history) |
| `created_at` | timestamp | |
| `updated_at` | timestamp | |

### `tags` collection (extension)

Add one nullable field:
- `parent_episode_id` UUID \| null — FK to `episodes.id`. When set, the tag is an "occurrence" of that episode on its day. When null, the tag is a free-standing day-marker.

No other changes to the tags schema. The 8-category enum from [ADR 0004](../../decisions/0004-tag-provenance-date-joins-and-tag-hierarchy.md) stays locked.

### The conceptual model (resolved 2026-06-02)

| Concept | Duration | Stored as | Example |
|---|---|---|---|
| Tag (standalone) | 1 day | Tag row, parent_episode_id=null | "bad headache today" |
| Gebeurtenis | 1 day | Tag row, category=`gebeurtenis` | "wedding day", "diagnosis day" |
| Interventie (1-day) | 1 day | Tag row, category=`interventie`, optional parent_episode_id | "paracetamol vandaag", "doctor visit" |
| Episode (life event) | multi-day | Episode row, category=`levensgebeurtenis` | "vakantie Texel 2026-07-15 → 2026-07-22" |
| Episode (intervention) | multi-day | Episode row, category=`interventie` | "Coaching met Sarah, 6 weken", "Citalopram, ongoing" |
| Linked tag (occurrence) | 1 day | Tag row + parent_episode_id set | "Coaching session today" linked to "Coaching met Sarah" episode |

Decision rule the user applies in the moment: **"Does this thing have a start AND an end (or is it ongoing)? If yes, episode. If it's just today, tag."** Interventie is orthogonal to duration — a doctor visit is a one-day interventie tag; a coaching program is a multi-day interventie episode.

## UI shape

### Context tab — Periodes section, grouped by category

```
[ Context ]   [ Vandaag ]   [ Tijdlijn ]

PERIODES

  [+ Nieuwe interventie]  [+ Nieuwe periode]

  Interventies (actief)
    · Coaching met Sarah
      2026-04-01 → lopend
    · Ergotherapie
      2026-05-15 → lopend

  Interventies (afgerond)
    · Citalopram afbouw
      2025-11-01 → 2026-01-31

  Levensgebeurtenissen (actief)
    · Vakantie Texel
      2026-07-15 → 2026-07-22
```

Resolved 2026-06-02 against alternatives "timeline-style bands" and "calendar-month grid". List view is the cleanest for brainfog (scan one column, tap to edit). The timeline visualisation lives on Tijdlijn, not on Context. Inside Context the heading hierarchy is: h2 "Periodes" (the section) → h3 "Interventies (actief)" etc. (the sub-groups within Periodes). v1.6 will add a sibling h2 "Agenda" (or similar) for Calendar bindings under the same Context tab.

Active episodes (end_date null OR end_date >= today) at top, past below. Tap an episode → detail/edit screen. Tap "+ Nieuwe" → create form.

### Episode detail/edit screen

Fields: label, category (read-only after create — changing category is confusing), start_date picker, end_date picker (optional, with "lopend" toggle for ongoing), description textarea, [v1.6: calendar binding], "Tags die hierbij horen" list (read-only in v1.5 — linking is from the tag side, see below), archive button.

### Tag-to-episode linking

Daily-flow tagging stays unchanged — inline-tag-creation in Vandaag does NOT gain a "link to episode" step (kept lightweight for the sub-10-second flow).

Linking happens in two places:
1. **From the Context tab's episode detail view** — "Voeg gekoppelde tag toe": pick from existing tags OR create a new tag with the parent set.
2. **From the inline tag editor** (future, v1.5b): a tag's detail view in the Settings → Tag-beheer screen gets a "behoort bij" picker.

For v1.5 the first path is the only one. Heavy management (recategorize, delete, mass-link) ships in v1.5b with the tag-management Settings screen.

## Out of scope (v1.5)

- **Calendar binding** (Google Calendar → episode). Deferred to v1.6. `calendar_binding` JSON column reserved but always null. The killer brainfog-relief feature ("the calendar already knows") gets its own UX design.
- **Episode categories beyond interventie + levensgebeurtenis**. `project` (long-running personal projects like "move house") and `patroon` (recurring rules like "weekends partner away") deferred to v2.
- **Episode-specific fields**: dosage, frequency, practitioner. Deferred. v1.5 keeps the schema tight: label + dates + description.
- **Hard delete of episodes**. v1.5 uses archive (soft delete). Hard delete via Directus admin only.
- **Bulk operations** on episodes or linked tags.
- **LLM-driven episode inference from notes** ("I see you mentioned coaching three days in a row, want to create a coaching episode?"). v2.

## Test plan (sketch — to be detailed by step files)

This feature is large enough for multiple step files. Tentative split:

| Step | Scope | Test layers |
|---|---|---|
| `step-1-episode-schema.md` | Directus collection + `parent_episode_id` migration scripts; Episode domain validators (`validateEpisodeLabel`, `validateEpisodeCategory`, `validateDateRange`) | Vitest unit |
| `step-2-episodes-api.md` | `src/lib/api/episodes.ts` (read/create/update/archive); `src/app/api/episodes/route.ts` + `[id]/route.ts` | Vitest unit (lib) + route handler |
| `step-3-periodes-tab-list.md` | New Context tab in TodayShell + ContextView component (Periodes section grouped by category) | Vitest component + e2e for tab nav |
| `step-4-episode-create-edit.md` | Episode form (create + edit), archive button, ongoing-toggle for end_date | Vitest component + e2e for happy-path round-trip |
| `step-5-tag-episode-linking.md` | "Voeg gekoppelde tag toe" affordance in episode detail; create-with-parent + link-existing paths | Vitest component + route extension |

## Acceptance criteria (feature level)

- [x] AC-F1: `episodes` collection exists in Directus; migration script in `directus/scripts/` is idempotent. (Step-1, 36fdadb; live + verified by `verify-schema.mjs` 39/39)
- [x] AC-F2: `tags.parent_episode_id` field exists; existing tag rows are unaffected (all null). (Step-1, 36fdadb; live + verified by `verify-schema.mjs`)
- [x] AC-F3: Context tab appears as the third top-level surface; tab order is Context / Vandaag / Tijdlijn (Vandaag centred for thumb balance). (Step-3 + 2026-06-02 evening rename; live + verified by today-shell + context-view tests)
- [x] AC-F4: Inside the Context tab, the Periodes section groups episodes by category × active/afgerond. (Step-3 + rename; h2 "Periodes" + 4 h3 sub-groups in documented order — Interventies actief → Interventies afgerond → Levensgebeurtenissen actief → Levensgebeurtenissen afgerond)
- [x] AC-F5: Create-episode form supports both categories; end_date is optional with a "lopend" affordance. (Step-4, 4be3266; EpisodeFormSheet with category locked from the launcher, lopend toggle defaulting ON in create + mirroring initialEpisode in edit, end_date input revealed when lopend OFF. 19 component tests cover the surface.)
- [x] AC-F6: Episode archive is reversible (soft delete only). (Step-2 + step-4; Step-4 wires the Archiveer button in the edit form. Un-archive surface ships in v1.5b but the data path is reversible today via direct PATCH.)
- [x] AC-F7: From an episode detail, the user can attach an existing tag or create a new tag with the parent set. The tag appears in the episode's "Tags die hierbij horen" list. (Step-5; LinkedTagsSection + TagPickerSheet hosted inside EpisodeFormSheet edit-mode; one-round-trip inline-create + silent re-parent across episodes; verified by component tests + extended episodes-smoke `8a-8d`)
- [ ] AC-F8: Daily-flow tagging in Vandaag is UNCHANGED — no regression, no new affordance, no extra taps. (Vandaag is now the CENTRE tab; the daily flow itself is untouched.)
- [x] AC-F9: Server-rendered Context tab data flows through to display without local-state shadow (same prop-driven pattern as TodayShell and TimelineView — necessary for router.refresh to move the UI). (Step-3, ec25924; page.tsx → TodayShell → ContextView prop chain, no useState shadow)
- [x] AC-F10: All v1 surfaces (Vandaag, Tijdlijn) continue working with or without episodes in the DB. (Step-3, ec25924; verified by existing TodayShell + TimelineView tests staying green, plus auth-smoke + episodes-smoke post-deploy)

## Resolved decisions (2026-06-02)

All open questions from the original draft are settled:

- **Episode label max length**: **40 chars, no word-count limit**. Same character ceiling as tag-label for scannability; word-count constraint dropped so natural 3-4-word episode names ("Coaching met Sarah", "Wekelijkse fysio bij Marieke") pass. Anything longer or more narrative belongs in `description`.
- **Episode-archive semantics on linked tags**: **keep the FK**. Tags retain `parent_episode_id` pointing at the archived episode. Tag remains usable in the daily flow (parent state is metadata only). Un-archive restores the relationship visually on the timeline overlay.
- **Renaming an episode**: **propagates globally**. Label is a display string; references are by id. Renaming updates the label everywhere — list view, timeline overlay, exports. Same model as tag-label renames.
- **Future-dated episodes**: **allowed**. `start_date` has no constraint relative to today. The timeline overlay simply won't render a band until the date is in range.

## References

- [ADR 0006](../../decisions/0006-three-surface-architecture.md) — three-surface architecture decision (Vandaag / Periodes / Tijdlijn).
- [features/tag-recency-sort/](../tag-recency-sort/) — v1.5a sibling, ships first.
- [features/timeline-episode-overlay/](../timeline-episode-overlay/) — v1.5 sibling, ships after this feature.
- [features/tag-management-settings/](../tag-management-settings/) — v1.5b follow-up for heavy tag management.
- [roadmap.md](../../roadmap.md) — where this sits in the larger plan.

## History

- 2026-05-31: conceived as `features/context-tab/` with Episode + Occurrence model.
- 2026-06-02 (AM): brainstorm session resolved naming ("Verloop"), data model (single polymorphic Episode collection; no separate Occurrence type — tags-with-parent ARE the occurrences), categories (interventie + levensgebeurtenis only for v1.5), and UX shape (grouped list, not bands). `features/context-tab/` retired; this file is the replacement.
- 2026-06-02 (PM): tab label revised "Verloop" → **Periodes** after a second pass. "Verloop" rejected for the expiry/decay echo ("verloopdatum"), clinical lean, and abstraction. Folder slug `verloop-and-episodes/` kept as an internal identifier for git-history continuity.
- 2026-06-02 (evening): tab label revised "Periodes" → **Context** as the final structural refinement. The tab is named for the container abstraction (Context = the bigger picture stuff that affects daily scores); Periodes is preserved as a section heading inside the tab. This sets up v1.6 Calendar bindings and v2 project context as sibling sections under the same Context tab without further rename cycles. Tab order also fixed: **Context / Vandaag / Tijdlijn**, with Vandaag centre-positioned for thumb balance on the daily-flow action.
