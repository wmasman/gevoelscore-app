# Roadmap

> Single navigable index of gevoelscore work: shipped, in flight, ready to plan, designed-but-not-detailed, and longer-term vision. Each entry links to its detailed doc. Update statuses inline when items move between sections.

This doc supplements [REQUIREMENTS.md](REQUIREMENTS.md) and [app_brief_gevoelscore.md](app_brief_gevoelscore.md). The brief defines what v1 IS; this roadmap tracks where work currently sits. When the two disagree (e.g. v1 scope vs. a new feature), the disagreement is flagged in the relevant feature README and resolved explicitly — never smuggled.

---

## In flight

| Item | Detail | Notes |
|---|---|---|
| Soak-test mode | [memory: project-soak-test-mode](../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/project_soak_test_mode.md) | iOS PWA usage gathers friction signal. Quick-entry popout + audit fixes (Days 0–5) shipped 2026-05-31. |

## Ready to plan (next)

Items here are scoped enough that the next step is `/plan-feature` to produce a step file with acceptance criteria + test plan.

| Item | Doc | Version | Size |
|---|---|---|---|
| Inline tag creation | [features/inline-tag-creation/](features/inline-tag-creation/) | v1 | Small (single step file) |
| Timeline gap indicator | [features/timeline-gap-indicator/](features/timeline-gap-indicator/) | v1 | Small (single step file) |

## Designed (architecture set, brainstorm pending)

Items here have an architectural decision (often an ADR) but need a design session before `/plan-feature` can run — usually because naming, conceptual model, or data shape is still open.

| Item | Doc | Version | What's pending |
|---|---|---|---|
| Three-surface architecture (Vandaag / Context / Tijdlijn) | [ADR 0006](decisions/0006-three-surface-architecture.md) | Decision | Accepted 2026-06-01 |
| Context tab — episodes + occurrences | [features/context-tab/](features/context-tab/) | v1.5 | Brainstorm: naming, conceptual model overlap with existing tag categories, data shape |

## Vision (design session needed first)

Items here are coherent enough to name but need a deeper conversation about tradeoffs (cost, privacy, locality, scope) before any commitment.

| Item | Doc | Likely version |
|---|---|---|
| Tag intelligence (auto-create from notes, surfacing algorithm, merge/consolidate, per-user universe) | [features/tag-intelligence/](features/tag-intelligence/) | v1.5 / v2 |
| Calendar import (Google/Apple, episode-bound only) | sub-section in [features/context-tab/](features/context-tab/) | v1.5 |
| Garmin integration (continuous-stream layer on timeline) | not yet documented | v2 |
| Multi-user / per-user data scoping (schema migration: `user_owner` on `tags`, `day_entries`) | not yet documented | v2 |

## Shipped (recent)

| Item | Doc | When |
|---|---|---|
| Quick-entry popout (Steps 0–5 + iOS popout-collapse fix) | [features/quick-entry-popout/](features/quick-entry-popout/) | 2026-05-29 → 2026-05-31 |
| Audit-fix week (Days 0–5: CI, manifest, contrast, auth hardening) | [audits/OPEN.md](audits/OPEN.md), [plans/2026-05-27-audit-remediation-and-standards-enforcement.md](plans/2026-05-27-audit-remediation-and-standards-enforcement.md) | 2026-05-27 → 2026-05-31 |
| Daily entry (Steps 0–6 + 4b) | [features/daily-entry/](features/daily-entry/) | 2026-05-28 |
| Frontend session persistence | [ADR 0005](decisions/0005-frontend-session-persistence.md) | 2026-05-28 |

---

## How to use this doc

- `Ready to plan` items are direct inputs to `/plan-feature`.
- `Designed` items need a design session (brainstorm conversation) before they can drop into `Ready to plan`. The "What's pending" column names the blockers.
- `Vision` items need a tradeoff conversation (cost, privacy, locality, scope) before they can drop into `Designed`. They often have concrete UX direction noted but no commitment on implementation.
- When a feature in `Ready to plan` or `Designed` contradicts something in [REQUIREMENTS.md](REQUIREMENTS.md) or the [brief](app_brief_gevoelscore.md) (e.g. v1 vs. v1.5 boundary), the feature README documents the disagreement explicitly. The roadmap's version column reflects the resolved answer.
- "Status" updates that are volatile (e.g. "in iOS soak", "deferred audit items") live in memory or the relevant feature README — not here. This doc is the index, not the news feed.
