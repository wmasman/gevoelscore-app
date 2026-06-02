# Roadmap

> Single navigable index of gevoelscore work: shipped, in flight, ready to plan, designed-but-not-detailed, and longer-term vision. Each entry links to its detailed doc. Update statuses inline when items move between sections.

This doc supplements [REQUIREMENTS.md](REQUIREMENTS.md) and [app_brief_gevoelscore.md](app_brief_gevoelscore.md). The brief defines what v1 IS; this roadmap tracks where work currently sits. When the two disagree (e.g. v1 scope vs. a new feature), the disagreement is flagged in the relevant feature README and resolved explicitly — never smuggled.

---

## In flight

| Item | Detail | Notes |
|---|---|---|
| Soak-test mode (v1) | [memory: project-soak-test-mode](../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/project_soak_test_mode.md) | iOS PWA usage gathering friction signal. v1 complete: quick-entry popout, inline tag creation, timeline gap indicator all live. |

## Ready to plan (next)

Items here are scoped enough that the next step is `/plan-feature` to produce a step file with acceptance criteria + test plan.

_(All v1.5 items above this line shipped 2026-06-02. Next ready-to-plan candidates pull from the **Vision** section below — promote whichever the user takes off the queue.)_

## Designed (architecture set, larger design still needed)

| Item | Doc | Version | What's pending |
|---|---|---|---|
| Three-surface architecture (Context / Vandaag / Tijdlijn) | [ADR 0006](decisions/0006-three-surface-architecture.md) | Decision | Accepted 2026-06-01; data-model + UX shape resolved 2026-06-02. Tab label evolved three times same day (Verloop → Periodes → Context). Final order **Context / Vandaag / Tijdlijn** with Vandaag centre-positioned for thumb balance. See [features/verloop-and-episodes/](features/verloop-and-episodes/). |

## Vision (design session needed first)

Items here are coherent enough to name but need a deeper conversation about tradeoffs (cost, privacy, locality, scope) before any commitment.

| Item | Doc | Likely version |
|---|---|---|
| Tag management in Settings (delete, recategorize, archive, accept suggestions) | _to be written_: `features/tag-management-settings/` | v1.5b |
| Calendar binding (Google Calendar → episode) | sub-section in [features/verloop-and-episodes/](features/verloop-and-episodes/) §Out of scope | v1.6 |
| Tag intelligence — LLM note-inference, correlation surfacing, merge/consolidate | [features/tag-intelligence/](features/tag-intelligence/) | v2 |
| Garmin integration (continuous-stream layer on timeline) | not yet documented | v2 |
| Multi-user / per-user data scoping (schema migration: `user_owner` on `tags`, `day_entries`) | not yet documented | v2 |
| Episode categories beyond v1.5: `project`, `patroon` | [features/verloop-and-episodes/](features/verloop-and-episodes/) §Out of scope | v2 |

## Shipped (recent)

| Item | Doc | When |
|---|---|---|
| Today-card ongoing-episodes region | follow-on note in [features/verloop-and-episodes/](features/verloop-and-episodes/) | 2026-06-02 (commits `dd51038` + `65ba2e8`; lists lopend + future-end-date episodes on the today-card with pencil-edit affordance) |
| Timeline episode overlay | [features/timeline-episode-overlay/](features/timeline-episode-overlay/) | 2026-06-02 (commit `1608d7a`; chart bands + linked-tag dots + heatmap stripes + per-category toggle, with in-place EpisodeFormSheet on band-tap) |
| Tag recency sort within category | [features/tag-recency-sort/](features/tag-recency-sort/) | 2026-06-02 (commit `426be73`; v1.5a slice of the tag-intelligence vision) |
| Context tab + Episodes (+ tag-linking) | [features/verloop-and-episodes/](features/verloop-and-episodes/) | 2026-06-02 (v1.5 anchor: 5 step files, all 10 ACs ticked; folder slug retained, user-facing tab is **Context** with Periodes as a section inside) |
| Timeline gap indicator | [features/timeline-gap-indicator/](features/timeline-gap-indicator/) | 2026-06-02 |
| Inline tag creation | [features/inline-tag-creation/](features/inline-tag-creation/) | 2026-06-01 |
| Quick-entry popout (Steps 0–5 + iOS popout-collapse fix) | [features/quick-entry-popout/](features/quick-entry-popout/) | 2026-05-29 → 2026-05-31 |
| Audit-fix week (Days 0–5: CI, manifest, contrast, auth hardening) | [audits/OPEN.md](audits/OPEN.md), [plans/2026-05-27-audit-remediation-and-standards-enforcement.md](plans/2026-05-27-audit-remediation-and-standards-enforcement.md) | 2026-05-27 → 2026-05-31 |
| Daily entry (Steps 0–6 + 4b) | [features/daily-entry/](features/daily-entry/) | 2026-05-28 |
| Frontend session persistence | [ADR 0005](decisions/0005-frontend-session-persistence.md) | 2026-05-28 |

## Retired / superseded

| Item | Doc | Reason |
|---|---|---|
| Context tab (Occurrence-type model only) | [features/context-tab/](features/context-tab/) (redirect page) | Superseded 2026-06-02 by [features/verloop-and-episodes/](features/verloop-and-episodes/). Note: the **tab name "Context" was eventually restored** after a three-pass same-day naming exercise (Verloop → Periodes → Context); what stayed retired is the Occurrence-type data model (tags-with-parent ARE the occurrences now) and the original folder location. |

---

## How to use this doc

- `Ready to plan` items are direct inputs to `/plan-feature`.
- `Designed` items have an ADR or vision doc but need a design session (brainstorm conversation) before they can drop into `Ready to plan`. The "What's pending" column names the blockers.
- `Vision` items need a tradeoff conversation (cost, privacy, locality, scope) before they can drop into `Designed`. They often have concrete UX direction noted but no commitment on implementation.
- When a feature in `Ready to plan` or `Designed` contradicts something in [REQUIREMENTS.md](REQUIREMENTS.md) or the [brief](app_brief_gevoelscore.md) (e.g. v1 vs. v1.5 boundary), the feature README documents the disagreement explicitly. The roadmap's version column reflects the resolved answer.
- "Status" updates that are volatile (e.g. "in iOS soak", "deferred audit items") live in memory or the relevant feature README — not here. This doc is the index, not the news feed.
