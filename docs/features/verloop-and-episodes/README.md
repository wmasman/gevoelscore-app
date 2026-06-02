# Periodes tab + Episodes

**Feature:** The v1.5 anchor. Adds a new third top-level surface (Periodes) for managing multi-day Episodes — interventions (coaching, physio, ergo, medication courses) and life events with duration (holidays, partner-away weekends, big work projects). Adds a new `episodes` Directus collection, a new nullable `tags.parent_episode_id` FK so single-day tags can hang off an ongoing episode as occurrences, and the Periodes-tab UI for episode CRUD + tag-linking.
**Version:** v1.5
**Status:** Designed — brainstorm resolved 2026-06-02; tab label finalised 2026-06-02 (revised from "Verloop" → "Periodes"). Ready for step files (multi-step feature).
**Parent docs:** [ADR 0006](../../decisions/0006-three-surface-architecture.md) (three-surface architecture) · [REQUIREMENTS.md](../../REQUIREMENTS.md) · [design/brief.md](../../design/brief.md) · [features/tag/](../tag/) (Tag domain — referenced for the new `parent_episode_id` field)

> **Folder slug note**: this folder is `features/verloop-and-episodes/` for git-history continuity. The user-facing tab label is **Periodes**. Do not rename the folder; treat the slug as an internal identifier only.

---

## Naming

- Tab name: **Periodes** (Dutch, "periods"). Final resolution 2026-06-02 after a second pass over "Verloop" (the earlier choice) — rejected because (a) "verloop" carries an expiry/decay echo via "verloopdatum", (b) it leans too clinical for a tab that also holds non-medical entries like a holiday, and (c) "Periodes" pictures the contents instantly: this is where date-range things live. The narrative weight lives in the **content** and on **Tijdlijn**; the tab label just needs to point cleanly.
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

### Periodes tab — list view, grouped by category

```
[+ Nieuwe interventie]  [+ Nieuwe periode]

INTERVENTIES (actief)
  · Coaching met Sarah
    2026-04-01 → lopend
  · Ergotherapie
    2026-05-15 → lopend

INTERVENTIES (afgerond)
  · Citalopram afbouw
    2025-11-01 → 2026-01-31

LEVENSGEBEURTENISSEN
  · Vakantie Texel
    2026-07-15 → 2026-07-22
```

Resolved 2026-06-02 against alternatives "timeline-style bands" and "calendar-month grid". List view is the cleanest for brainfog (scan one column, tap to edit). The timeline visualisation lives on Tijdlijn, not on Periodes.

Active episodes (end_date null OR end_date >= today) at top, past below. Tap an episode → detail/edit screen. Tap "+ Nieuwe" → create form.

### Episode detail/edit screen

Fields: label, category (read-only after create — changing category is confusing), start_date picker, end_date picker (optional, with "lopend" toggle for ongoing), description textarea, [v1.6: calendar binding], "Tags die hierbij horen" list (read-only in v1.5 — linking is from the tag side, see below), archive button.

### Tag-to-episode linking

Daily-flow tagging stays unchanged — inline-tag-creation in Vandaag does NOT gain a "link to episode" step (kept lightweight for the sub-10-second flow).

Linking happens in two places:
1. **From a Periodes episode's detail view** — "Voeg gekoppelde tag toe": pick from existing tags OR create a new tag with the parent set.
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
| `step-3-periodes-tab-list.md` | New tab in TodayShell + PeriodesView component (list grouped by category) | Vitest component + e2e for tab nav |
| `step-4-episode-create-edit.md` | Episode form (create + edit), archive button, ongoing-toggle for end_date | Vitest component + e2e for happy-path round-trip |
| `step-5-tag-episode-linking.md` | "Voeg gekoppelde tag toe" affordance in episode detail; create-with-parent + link-existing paths | Vitest component + route extension |

## Acceptance criteria (feature level)

- [x] AC-F1: `episodes` collection exists in Directus; migration script in `directus/scripts/` is idempotent. (Step-1, 36fdadb; live + verified by `verify-schema.mjs` 39/39)
- [x] AC-F2: `tags.parent_episode_id` field exists; existing tag rows are unaffected (all null). (Step-1, 36fdadb; live + verified by `verify-schema.mjs`)
- [ ] AC-F3: Periodes tab appears as the third top-level surface; tab order is Vandaag / Periodes / Tijdlijn.
- [ ] AC-F4: List view groups episodes by category, active first.
- [ ] AC-F5: Create-episode form supports both categories; end_date is optional with an "lopend" affordance.
- [x] AC-F6: Episode archive is reversible (soft delete only). (Step-2, c6b31c2; PATCH archived_at: ISO archives, PATCH archived_at: null un-archives — verified end-to-end by episodes-smoke.)
- [ ] AC-F7: From an episode detail, the user can attach an existing tag or create a new tag with the parent set. The tag appears in the episode's "Tags die hierbij horen" list.
- [ ] AC-F8: Daily-flow tagging in Vandaag is UNCHANGED — no regression, no new affordance, no extra taps.
- [ ] AC-F9: Server-rendered Periodes tab data flows through to display without local-state shadow (same prop-driven pattern as TodayShell and TimelineView — necessary for router.refresh to move the UI).
- [ ] AC-F10: All v1 surfaces (Vandaag, Tijdlijn) continue working with or without episodes in the DB.

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
