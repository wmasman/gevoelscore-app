# Verloop tab + Episodes

**Feature:** The v1.5 anchor. Adds a new third top-level surface (Verloop) for managing multi-day Episodes — interventions (coaching, physio, ergo, medication courses) and life events with duration (holidays, partner-away weekends, big work projects). Adds a new `episodes` Directus collection, a new nullable `tags.parent_episode_id` FK so single-day tags can hang off an ongoing episode as occurrences, and the Verloop-tab UI for episode CRUD + tag-linking.
**Version:** v1.5
**Status:** Designed — brainstorm resolved 2026-06-02. Ready for step files (multi-step feature).
**Parent docs:** [ADR 0006](../../decisions/0006-three-surface-architecture.md) (three-surface architecture) · [REQUIREMENTS.md](../../REQUIREMENTS.md) · [design/brief.md](../../design/brief.md) · [features/tag/](../tag/) (Tag domain — referenced for the new `parent_episode_id` field)

---

## Naming

- Tab name: **Verloop** (Dutch, "course / progression / trajectory"). Resolved 2026-06-02 against alternatives *Context*, *Achtergrond*, *Periodes*. Carries the chronic-illness narrative tone and pairs naturally with the timeline ("the Tijdlijn IS my Verloop").
- Data type: **Episode** (English in code, "interventie" / "levensgebeurtenis" in user copy).
- Junction: a Tag's optional pointer to its parent episode is called `parent_episode_id`.

## Data model

### `episodes` collection (new)

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | PK |
| `label` | string | Trimmed, non-empty, max 60 chars (looser than tag-label since episodes get longer names: "Coaching met Sarah", "Citalopram afbouw") |
| `category` | enum | `interventie` \| `levensgebeurtenis`. v1.5 enum is tight; `project` + `patroon` deferred to v2 (see "Out of scope") |
| `start_date` | DATE | ISO YYYY-MM-DD |
| `end_date` | DATE \| null | null = ongoing |
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

### Verloop tab — list view, grouped by category

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

Resolved 2026-06-02 against alternatives "timeline-style bands" and "calendar-month grid". List view is the cleanest for brainfog (scan one column, tap to edit). The timeline visualisation lives on Tijdlijn, not here.

Active episodes (end_date null OR end_date >= today) at top, past below. Tap an episode → detail/edit screen. Tap "+ Nieuwe" → create form.

### Episode detail/edit screen

Fields: label, category (read-only after create — changing category is confusing), start_date picker, end_date picker (optional, with "lopend" toggle for ongoing), description textarea, [v1.6: calendar binding], "Tags die hierbij horen" list (read-only in v1.5 — linking is from the tag side, see below), archive button.

### Tag-to-episode linking

Daily-flow tagging stays unchanged — inline-tag-creation in Vandaag does NOT gain a "link to episode" step (kept lightweight for the sub-10-second flow).

Linking happens in two places:
1. **From a Verloop episode's detail view** — "Voeg gekoppelde tag toe": pick from existing tags OR create a new tag with the parent set.
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
| `step-3-verloop-tab-list.md` | New tab in TodayShell + VerloopView component (list grouped by category) | Vitest component + e2e for tab nav |
| `step-4-episode-create-edit.md` | Episode form (create + edit), archive button, ongoing-toggle for end_date | Vitest component + e2e for happy-path round-trip |
| `step-5-tag-episode-linking.md` | "Voeg gekoppelde tag toe" affordance in episode detail; create-with-parent + link-existing paths | Vitest component + route extension |

## Acceptance criteria (feature level)

- [ ] AC-F1: `episodes` collection exists in Directus; migration script in `directus/scripts/` is idempotent.
- [ ] AC-F2: `tags.parent_episode_id` field exists; existing tag rows are unaffected (all null).
- [ ] AC-F3: Verloop tab appears as the third top-level surface; tab order is Vandaag / Verloop / Tijdlijn.
- [ ] AC-F4: List view groups episodes by category, active first.
- [ ] AC-F5: Create-episode form supports both categories; end_date is optional with an "lopend" affordance.
- [ ] AC-F6: Episode archive is reversible (soft delete only).
- [ ] AC-F7: From an episode detail, the user can attach an existing tag or create a new tag with the parent set. The tag appears in the episode's "Tags die hierbij horen" list.
- [ ] AC-F8: Daily-flow tagging in Vandaag is UNCHANGED — no regression, no new affordance, no extra taps.
- [ ] AC-F9: Server-rendered Verloop tab data flows through to display without local-state shadow (same prop-driven pattern as TodayShell and TimelineView — necessary for router.refresh to move the UI).
- [ ] AC-F10: All v1 surfaces (Vandaag, Tijdlijn) continue working with or without episodes in the DB.

## Open questions

- **Episode label max length**: currently proposed at 60 chars. Tags are 40 / 2 words; episodes are longer narratives. Verify in step-1 whether 60 is enough (or 80).
- **Episode-archive semantics on linked tags**: if I archive an episode, what happens to its linked tags? Options: (a) tags keep their `parent_episode_id` pointing at the archived episode, hidden in UI but recoverable on un-archive; (b) tags get unlinked (parent_episode_id → null) on episode archive. Recommendation: (a). Confirm in step-1.
- **Renaming an episode** — does the rename propagate to historical timeline labels? Probably yes (the label is just a display string; nothing references it by value). Confirm in step-4.

## References

- [ADR 0006](../../decisions/0006-three-surface-architecture.md) — three-surface architecture decision (Vandaag / Verloop / Tijdlijn).
- [features/tag-recency-sort/](../tag-recency-sort/) — v1.5a sibling, ships first.
- [features/timeline-episode-overlay/](../timeline-episode-overlay/) — v1.5 sibling, ships after this feature.
- [features/tag-management-settings/](../tag-management-settings/) — v1.5b follow-up for heavy tag management.
- [roadmap.md](../../roadmap.md) — where this sits in the larger plan.

## History

- 2026-05-31: conceived as `features/context-tab/` with Episode + Occurrence model.
- 2026-06-02: brainstorm session resolved naming ("Verloop"), data model (single polymorphic Episode collection; no separate Occurrence type — tags-with-parent ARE the occurrences), categories (interventie + levensgebeurtenis only for v1.5), and UX shape (grouped list, not bands). `features/context-tab/` retired; this file is the replacement.
