# Tag intelligence

**Feature:** A growing intelligence layer around the tag system. Auto-create tags from notes, algorithmic surfacing of relevant tags per day, merge/group/consolidate operations, per-user tagging universe. The unifying ambition: the system thinks along, so the tag step takes less cognitive effort, not more.
**Version:** v1.5 (parts) / v2 (parts) — see "Component breakdown"
**Status:** Vision — design session needed before commitment. Sub-pieces are not yet scoped.
**Parent docs:** [REQUIREMENTS.md](../../REQUIREMENTS.md) · [design/brief.md](../../design/brief.md) · [features/tag/](../tag/) (Tag domain) · [features/inline-tag-creation/](../inline-tag-creation/) (the small v1 feature this vision is north star for)

---

## Guiding principle

> The tagging step should make things *easier*, not harder. The system thinks along: it surfaces tags you're likely to pick, infers tags from notes you already wrote, learns the vocabulary you actually use. Adding tagging affordances must always either leave the score-only path unchanged OR actively reduce friction in the tag step.

This is the north star for every tagging-related feature. Even the small [inline-tag-creation](../inline-tag-creation/) feature in v1 is held to it (it removes a dead-end empty state and a context-switch to the admin UI — net friction reduction).

## Why a separate vision doc

Tag-domain (`features/tag/`) covers the entity. Inline-tag-creation (`features/inline-tag-creation/`) covers the immediate UI gap. This doc covers everything that turns the tag system from "a dropdown" into "a personal vocabulary that learns": that is a multi-feature, multi-version effort with cost, privacy, and locality tradeoffs that need their own conversation.

## Component breakdown

### A. Auto-create tags from notes (v2-likely)

The note field in Vandaag accepts free text. After save, an inference step proposes (or directly creates) tags that match the content. Example: "ging vandaag naar de fysio" → suggests `fysiotherapie` tag (creating it if not present, attaching it if so).

**Open tradeoffs (require a dedicated design session before commitment):**

- **Locality.** Local model on device (privacy-preserving but limited capability), local server-side model (Directus extension or sidecar — adds infra), or external API call (best capability, cost, data exits device).
- **Privacy posture.** Notes can contain sensitive medical content. An external LLM call ships that content to a third party. Even if data is not stored upstream, the trust posture changes materially. The brief's privacy stance is strict.
- **Cost.** External APIs have per-call cost. With multi-user, costs scale linearly with daily-active users.
- **Latency.** Inference inline with save adds noticeable latency. Async post-save inference (background job) keeps the save fast but means tags appear later.
- **Opt-in vs. default.** Strong default toward opt-in — the user actively turns on note-inference per their privacy comfort.
- **Trust calibration.** Auto-attach (high confidence) vs. suggest-and-confirm (low cognitive load but adds a step) vs. show-as-pending-pill (zero-tap default if user does nothing).

**Decision blockers:** at least the locality + privacy questions must be resolved before this feature can be scoped. Worth its own brainstorm session.

### B. Algorithmic surfacing (v1.5 / v2)

Show the most-likely-relevant tags first when the tag step opens. Signals to combine:

- Recency (last used in the past N days)
- Frequency (lifetime count)
- Score correlation (tags that co-occur with this score range)
- Day-of-week patterns
- Time-of-day (where the user logs in their day)
- Note-content correlation (if a note is already typed, tags that historically co-occur with similar notes)

The simple v1.5 version is recency + frequency sort (no ML). The v2 version layers correlation signals as the user accumulates more data. **Both are the same problem in different stages of evolution** — design the UI shape so the surfacing algorithm can swap underneath without UI change.

The minimum surfacing UX: a horizontal strip of "Recent / Often used" tags above the category list. Tapping one selects it. Tapping the category header still works as today for browsing the full set. This shape works for both the simple and ML versions.

### C. Merge / group / consolidate (v2)

The user's tag vocabulary drifts over time: near-duplicates (`hoofdpijn`, `hoofdpijntje`, `migraine-achtig`), categories that turn out to overlap, tags that get retired. Admin operations:

- Rename (label only, keeps id and all join rows)
- Merge two tags (id A absorbs id B, all `day_entries_tags` rows for B repoint to A, B archived)
- Group into a parent (introduces a tag hierarchy — overlaps with [ADR 0004](../../decisions/0004-tag-provenance-date-joins-and-tag-hierarchy.md))
- Archive (already exists at the schema level, no UI yet)

These need UI (probably in the future settings tab) and a Directus migration that rewrites join rows when ids merge. Low-frequency operation — the UX can be slightly heavier than the daily-flow surfaces.

### D. Per-user tag universe (v2)

Multi-user v2. Today's `Tag` schema has no `user_owner` field — same shared-data limitation as `day_entries`. Adding it is a schema migration + backfill (everything Willem currently has → Willem-owned).

The user's framing: *"Each user of the app will need to be able to create their own tagging universe and infrastructure fitting their subjective situation and language and preferred exact use of the app."*

This means:

- Per-user tag namespace (two users can both have a `pacing` tag with different ids and different meanings)
- Per-user category enum extension? Or do all users share the 8-category enum from [ADR 0004](../../decisions/0004-tag-provenance-date-joins-and-tag-hierarchy.md)? Open question — leaving the enum shared is simpler; letting users define their own categories is more personal but adds taxonomic chaos.
- Per-user surfacing models (component B is trained on this user's data only)

This is the largest piece. Gated on a multi-user launch decision.

## Constraints inherited by all components

- **Score-only path is sacrosanct.** Whatever this layer does, the user who taps a score and dismisses takes the same number of taps as today.
- **Dedup is server-side.** Whether a tag is created from the inline UI, from auto-inference, or from a future import path, case-insensitive label match within category returns the existing id. The dedup logic lives in the `POST /api/tags` route (created in [inline-tag-creation](../inline-tag-creation/)) and is reused by every downstream creator.
- **No LLM calls in v1.** The cost/privacy/locality conversation has to happen before any external call ships. Local heuristics (recency, frequency, simple co-occurrence) are LLM-free and can ship sooner.
- **Honest UX about what's inferred.** If a tag was auto-attached by the system, the UI shows that clearly (e.g. dotted outline, "auto" pill) so the user can correct it without ambiguity.

## What's NOT part of this vision

- The Tag entity itself (covered by [features/tag/](../tag/)).
- The inline create UI (covered by [features/inline-tag-creation/](../inline-tag-creation/) — this vision's small-step sibling).
- The tag-vs-episode boundary (covered by [features/context-tab/](../context-tab/) — sibling vision, brainstorm pending).
- Streaming biometric data (Garmin etc) — different shape entirely, see [roadmap](../../roadmap.md).

## Brainstorm session topics

When this vision moves toward `/plan-feature`, the conversations needed are:

1. **Locality + privacy for note-inference.** Local model vs. external API vs. no-inference-only-surfacing. (Component A blocker.)
2. **Surfacing UX shape.** Horizontal strip above categories vs. mixed into category lists vs. separate "voor jou" section. (Component B.)
3. **When does `user_owner` get added.** Tied to the multi-user launch decision. (Component D blocker.)
4. **Tag hierarchy** — does merge/group/consolidate (Component C) introduce a parent-child relation on tags, or stay flat? Touches [ADR 0004](../../decisions/0004-tag-provenance-date-joins-and-tag-hierarchy.md).

## References

- [features/inline-tag-creation/](../inline-tag-creation/) — the v1 small step held to this vision's principle.
- [features/context-tab/](../context-tab/) — sibling vision, shares the tag-vs-episode boundary.
- [roadmap.md](../../roadmap.md) — where this sits in the larger plan.
