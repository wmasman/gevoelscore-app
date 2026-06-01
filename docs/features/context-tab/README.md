# Context tab (working name — brainstorm pending)

**Feature:** The third top-level surface introduced by [ADR 0006](../../decisions/0006-three-surface-architecture.md). Home for range entities (events, intervention episodes), calendar/import bindings, and any other longer-form context the user attaches to their tracking. Distinct from Vandaag (quick log) and Tijdlijn (synthesis).
**Version:** v1.5 (brings forward what the [brief](../../app_brief_gevoelscore.md) named as v1.5 — projecten, agenda-koppeling, interventies)
**Status:** Vision — naming + conceptual model brainstorm pending. NOT yet ready for `/plan-feature`. See "What needs a brainstorm session" below.
**Parent docs:** [ADR 0006](../../decisions/0006-three-surface-architecture.md) · [REQUIREMENTS.md](../../REQUIREMENTS.md) · [design/brief.md](../../design/brief.md)

---

## What's known

The architecture is decided ([ADR 0006](../../decisions/0006-three-surface-architecture.md)). The data model has a clear shape:

- **Tag** = atomic per-day marker, no parent. Existing model, unchanged.
- **Episode** = range entity (start/end, category, optional dosage/frequency, optional calendar-series binding or recurrence rule). Lives in its own Directus collection.
- **Occurrence** = atomic per-day marker that belongs to an Episode. Populated by manual entry, calendar import bound to the episode, or recurrence rule.

The third tab manages episodes and their bindings. The timeline reads from both tags and episodes for its synthesis view. The daily flow (Vandaag) is unaffected.

The motivating use case from the design conversation: a 6-week coaching period with weekly sessions. The 6-week range is one episode; the individual sessions are occurrences. Binding the episode to a Google Calendar series lets the calendar do the remembering, so the user does not have to context-switch into their calendar app every day they log retroactively. **The mental-load relief is the primary justification for calendar import**, not convenience.

## What needs a brainstorm session

These items block `/plan-feature`. Resolve in a dedicated design conversation before scoping step files.

### 1. Naming of the third tab

"Context" is the working name. Candidates considered so far:

- **Context** — descriptive but flat; loanword reads fine in Dutch
- **Achtergrond** — Dutch, evokes "what was happening behind the score"
- **Verloop** — Dutch, evokes "course of treatment / progression"
- **Invloeden** — Dutch, evokes "what influences the score"
- (Things-3's analog is "Areas" — useful reference point but not necessarily the right metaphor here)

The right answer depends on which mental model the user holds: is this tab about *causes/influences* (medical framing), *the journey* (narrative framing), or *the things I'm tracking against* (Things-3-style "areas of life")?

### 2. Tag-categories vs. Episodes — conceptual overlap

[ADR 0004](../../decisions/0004-tag-provenance-date-joins-and-tag-hierarchy.md) locked the tag category enum including `gebeurtenis` and `interventie`. With episodes existing, those categories partially duplicate the new model.

The proposed-but-not-yet-decided resolution: tag-categories survive for one-off markers; episodes are canonical for multi-day or repeating things. But the boundary is fuzzy:

- "Paracetamol vandaag" — one-off interventie tag, or an occurrence of an ongoing "pain management" episode?
- "Visit to GP" — one-off gebeurtenis tag, or an occurrence of an ongoing "GP follow-ups" episode?
- "Holiday weekend" — gebeurtenis tag, or a short episode?

The brainstorm needs to produce:

- A clear decision rule the user can apply in the moment (without thinking)
- A migration path if `gebeurtenis` / `interventie` tag categories are deprecated (they shouldn't be, but the rule should make it obvious which to choose)
- Vocabulary that survives translation to the UI (the user shouldn't see "tag" vs. "episode" as a jargon distinction)

### 3. Data shape for Episode

Beyond `start_date`, `end_date`, `category`, the right fields depend on use case:

- **Interventions (medication):** dose, frequency, prescribing party, reason for stopping
- **Interventions (therapy):** practitioner, session frequency, modality (in-person/online), notes per session
- **Events (life milestones):** description, emotional valence (positive/negative/mixed), expected vs. unexpected
- **Events (recurring patterns):** "weekends partner away" — recurrence rule, not a single range

Designing for all of these at once produces a Directus form with 20 fields, most empty most of the time. The brainstorm needs to decide: one episode collection with optional fields and per-category UI? Or a few specialised collections (`intervention`, `life_event`, `recurring_pattern`)?

### 4. Calendar-binding configuration UX

Binding an episode to a Google Calendar series means:

- OAuth into Google Calendar (read-only scope)
- Picking a calendar
- Picking either a specific recurring series or a filter (events whose title matches a pattern)
- Choosing whether past events also import or only future ones
- Storing the binding so future syncs work

This is non-trivial UI. The brainstorm needs to decide whether v1.5 ships with manual-entry-only and the binding is v1.6, or whether the binding ships at the same time. Manual-entry-first is the lower-risk path; binding-first proves the brainfog-relief value sooner.

### 5. Timeline visualisation of three-layer overlay

Tags as dots, episode bands underneath the score line, occurrences as dots-on-bands. On a phone-width display, this risks visual noise. The brainstorm should produce a paper-sketch (or low-fi mock) of the timeline with all three layers populated, and decide:

- Visual weight order: which layer wins when they overlap?
- How to handle multiple concurrent episodes (stack the bands? thin them?)
- What happens when a tag and an occurrence are on the same day (one dot or two?)

## Out of scope of the brainstorm

- **Garmin / continuous-stream layer.** Defer until the three-layer overlay is proven readable.
- **Calendar import beyond Google.** Apple Calendar is a candidate; not the brainstorm topic. Start with Google.
- **Multi-user concerns.** Episode collection will need `user_owner` when multi-user lands. Same pattern as the rest of the schema. Not a brainstorm item.

## Build order (proposed, post-brainstorm)

1. Episode + Occurrence Directus collections + read API.
2. Context tab UI: list episodes, create episode, edit episode, archive.
3. Timeline read-side: render episode bands + occurrence dots on the existing timeline.
4. Manual-entry occurrences (button on Vandaag's tag step? on the context tab? on the timeline day-detail? — brainstorm topic).
5. Calendar binding (Google OAuth + scope, series picker, store binding, periodic sync).
6. (Future) Garmin continuous-stream layer.

## References

- [ADR 0006](../../decisions/0006-three-surface-architecture.md) — the architectural decision.
- [features/tag-intelligence/](../tag-intelligence/) — sibling vision; the tag-vs-episode boundary touches both.
- [roadmap.md](../../roadmap.md) — where this sits in the larger plan.
