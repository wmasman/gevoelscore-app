# ADR 0006: Three-surface architecture (Context / Vandaag / Tijdlijn)

- **Status**: Accepted
- **Date**: 2026-06-01 (decision); refined 2026-06-02 (data model + naming + categories; tab label evolved three times same day: Context (initial draft) → Verloop (brainstorm) → Periodes (revision) → **Context** (final, with Periodes preserved as a section heading inside the tab))
- **Version target**: **v1.5** (NOT v1 — see "Version-boundary nuance" below)
- **Builds on**: [ADR 0002](0002-pwa-with-directus-backend.md) (Next.js + Directus stack), [ADR 0004](0004-tag-provenance-date-joins-and-tag-hierarchy.md) (tag taxonomy), the design [brief](../design/brief.md) (thumb-first, restrained motion, no extra-screens-on-input principle)
- **Deciders**: Willem Masman (author), Claude (AI collaborator)

> **2026-06-02 refinement** (during the v1.5 brainstorm session):
> - The tab is named **Context** — back to the original ADR working name after a same-day three-pass revision (Context → Verloop → Periodes → **Context**). The final revision was structural: Periodes is now a *section heading inside* Context, not the tab label itself. The Context container is the right level of abstraction once the v1.6 Calendar bindings and v2 project context land as sibling sections under the same tab.
> - **Tab order in the bottom nav** (set by `today-shell.tsx`): Context / Vandaag / Tijdlijn. Vandaag is **centre-positioned** so the daily-flow action is thumb-balanced on both right-hand and left-hand grip; Context (less-frequent management) is left, Tijdlijn (less-frequent review) is right.
> - The data model is simpler than the original Episode + Occurrence pair: there is no separate Occurrence type. Tags get an optional `parent_episode_id` field, and **a tag with a parent IS the occurrence**. Episode is a single polymorphic collection (no separate intervention/event collections).
> - Episode categories for v1.5: `interventie` + `levensgebeurtenis` only. `project` + `patroon` deferred to v2.
> - Calendar binding deferred to v1.6; v1.5 ships manual-entry-only.
>
> See [features/verloop-and-episodes/](../features/verloop-and-episodes/) for the resolved feature plan (folder slug retained as an internal identifier; user-facing label is **Periodes**) and [features/context-tab/](../features/context-tab/) for the retired earlier draft. The architectural shape in the body of this ADR remains correct; only naming + the data-model details below have been simplified.

## Context

The app today (v1, shipped 2026-05-28 → 2026-05-31) has two surfaces: **Vandaag** (the quick-entry popout for score/note/tags) and **Tijdlijn** (the timeline read-view). This matches the [brief's v1 screens](../app_brief_gevoelscore.md) and [REQUIREMENTS.md "v1 screens"](../REQUIREMENTS.md).

Two roadmap directions create pressure on this shape:

1. **Interventions and events as context.** The user wants to capture multi-day events ("weekend partner away", "holiday", "lost job") and intervention episodes ("coaching with Sarah, started 2026-04-01, ongoing"; "physiotherapy 6 weeks") to overlay on the timeline. Score alone is one signal; the overlay is what turns the timeline from a diary into something actionable for chronic-illness self-management.

2. **Mental-load relief on input.** Asking the user to log every coaching session, every doctor visit, every medication change manually defeats the purpose. Calendar import (and eventually Garmin) should do the remembering. But import data needs a home that isn't Vandaag — the daily flow must stay sub-10-seconds.

The naive shapes both fail:

- **Extending the tagging step inside Vandaag** with date-range pickers bloats the brainfog-sensitive entry flow. Violates the cardinal principle ([brief §Cardinaal principe](../app_brief_gevoelscore.md)).
- **Adding modal screens on top of Vandaag** (a "+ event" button that opens a fullscreen form) violates the design brief's no-extra-screens-on-input principle and the spatial principle (thumb-first for input).

## Decision

The app splits into **three top-level surfaces**, each with one clear job:

1. **Vandaag** — quick log (score / note / tags). **Untouched by this ADR.** The cardinal principle (one tap, sub-10-seconds) holds; nothing layered on top.
2. **Context** (final — naming resolved 2026-06-02; see "Open questions" for the same-day Verloop → Periodes → Context history). Manages range entities: event date-ranges, intervention episodes, calendar / Garmin import bindings. Where multi-day and repeating things live. Periodes is now a section heading INSIDE this tab, not the tab label.
3. **Tijdlijn** — read-only synthesis. Score line + episode bands + occurrence dots + free-floating tag dots, all on one timeline.

The data model that supports this:

- **Tag** = atomic per-day marker, no parent. Existing model, unchanged. Used for spontaneous one-off things ("bad headache today", "took paracetamol").
- **Episode** = range entity. Has `start_date`, optional `end_date` (ongoing if null), `category` (initially: intervention or event — see "Open questions"), optional dosage/frequency fields, optional calendar-series binding or recurrence rule. Lives in its own Directus collection.
- **Occurrence** = atomic per-day marker that belongs to an Episode. Populated by manual entry, calendar import bound to the episode, or a recurrence rule defined on the episode.

The visual layering on the timeline that supports the synthesis:

- Tags as faint dots, one layer
- Episodes as bands underneath the score line, one layer
- Occurrences as dots *on* their band, one layer
- (Future) Continuous-stream data (Garmin) as background layer

Four visual layers stacked on the score line is the noise budget. Anything more drowns the score signal.

## Version-boundary nuance

The [brief](../app_brief_gevoelscore.md) is explicit:

> "v1 is een soepele UI die doet wat ik nu in Excel doe, beter. Niets meer. **De projecten, agenda-koppeling, Apple Health en Garmin uit de rest van dit document zijn vanaf v1.5 en verder.**"

The context tab brings forward what the brief named as v1.5 (projects/interventies/agenda-koppeling). **This ADR does not redefine v1.** The three-surface architecture is the v1.5 plan; the v1 app continues to operate as two surfaces (Vandaag + Tijdlijn) until the v1.5 work ships.

The architecture is declared now (rather than at v1.5 build time) because two upcoming v1 features — inline tag creation and timeline gap indicator — sit at the boundary and need to know which side of the v1/v1.5 line they're on. Both are v1; neither touches the Context tab.

## Options considered

### Option A — Extend tagging step with date-range capabilities

Pros: no new surface, reuses existing UI.
Cons: violates the cardinal principle (10-second flow), conflates per-day markers with multi-day ranges, no good place for calendar binding configuration.
Verdict: rejected.

### Option B — Modal screens on top of Vandaag

Pros: no new tab.
Cons: violates the no-extra-screens-on-input principle from the design brief, deep modal stacks are hostile to brainfog users, calendar-binding configuration doesn't belong layered over the daily flow.
Verdict: rejected.

### Option C — Three-surface architecture (chosen)

Pros: each surface has one job, Vandaag stays sub-10-seconds, context lives in a navigable place, timeline becomes the synthesis surface the brief always wanted it to be, episode/occurrence model handles parent/child cleanly.
Cons: adds nav-bar surface area (third tab), naming is open (see below), conceptual overlap with existing `gebeurtenis` / `interventie` tag categories needs to be resolved.
Verdict: accepted.

## Consequences

**Positive:**

- The brief's v1.5 ambition ("projecten, agenda-koppeling") now has a concrete architectural home.
- Calendar/Garmin imports get a natural place to be configured (per-episode binding), avoiding the noise of "import everything".
- Tag-categories `gebeurtenis` and `interventie` (locked in [ADR 0004](0004-tag-provenance-date-joins-and-tag-hierarchy.md)) survive — for one-off markers — but the canonical place for multi-day or repeating things moves to episodes.

**Open / to be brainstormed:**

- **Naming of the third tab.** ~~"Context" is descriptive but flat. Dutch candidates: *Context*, *Achtergrond*, *Verloop*, *Invloeden*. Things-3's analog is "Areas". A naming brainstorm is required before [features/context-tab/](../features/context-tab/) leaves the vision stage.~~ **Resolved 2026-06-02** after three same-day passes (Verloop → Periodes → Context). Final label: **Context**, with Periodes as a section heading inside.
- **Tag-category vs episode conceptual model.** When does something become an episode vs. a tag? Is "paracetamol vandaag" a one-off interventie tag or an occurrence of a long-running "pain management" episode? Needs a brainstorm session — flagged explicitly in [features/context-tab/](../features/context-tab/) so future-us doesn't accidentally deprecate the categories.
- **Data shape for `Episode`**. Fields beyond start/end/category/binding need to be designed against real cases (medication dose changes, coaching sessions with notes, weekend-partner-away as a recurring pattern).
- **Privacy posture for calendar import.** Event titles can contain sensitive medical content. Import is opt-in per episode (you bind one series at a time, not the whole calendar). Delete path: removing an episode removes its occurrences; removing the binding stops further imports but doesn't delete already-imported occurrences.

**Negative / costs:**

- Adds one tab to the nav. Three-tab nav is still well within UX norms but worth verifying against the brainfog-sensitive design principles when the tab is wired up.
- The episode/occurrence collections add schema work to the v1.5 release.
- The four-visual-layer timeline needs careful design at small phone widths to stay readable; revisit if it gets noisy.

**Out of scope of this ADR:**

- Tag intelligence (auto-create from notes, surfacing algorithm) is a separate vision — see [features/tag-intelligence/](../features/tag-intelligence/).
- Whether timeline should eventually become the home tab (with Vandaag as a quick-action from there) is an open future question, not decided here.

## References

- [features/context-tab/](../features/context-tab/) — vision README + the naming/concept brainstorm topics.
- [features/tag-intelligence/](../features/tag-intelligence/) — related vision, intentionally distinct.
- [roadmap.md](../roadmap.md) — places this ADR in context.
