# Roadmap

> Single navigable index of gevoelscore work: shipped, in flight, ready to plan, designed-but-not-detailed, and longer-term vision. Each entry links to its detailed doc. Update statuses inline when items move between sections.

This doc supplements [REQUIREMENTS.md](REQUIREMENTS.md) and [app_brief_gevoelscore.md](app_brief_gevoelscore.md). The brief defines what v1 IS; this roadmap tracks where work currently sits. When the two disagree (e.g. v1 scope vs. a new feature), the disagreement is flagged in the relevant feature README and resolved explicitly — never smuggled.

---

## In flight

| Item | Detail | Notes |
|---|---|---|
| Soak-test mode (v1 → v1.5c) | [memory: project-soak-test-mode](../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/project_soak_test_mode.md) | iOS PWA usage gathering friction signal. All v1 + v1.5 + v1.5a/b/c live; tag-merge soak (UI + brainfog-sensitive confirm flow) in progress on the user's iPhone PWA. |
| Calendar binding (v1.6) | [features/calendar-binding/](features/calendar-binding/) | Planning complete 2026-06-03. Feature folder + README + 4 step files (step-0 data model + step-1 OAuth/Settings/Context + step-2 cron/Today + step-3 timeline overlay) + 3 defer markers (step-4 v2 learned rules; step-5 v2 second provider; step-6 v1.6.1 calendar-bound episodes). Resolved 7 design decisions across 4 brainstorm conversations + 1 in-plan decision (Shape A event-side linking ships v1.6; Shape B episode-side binding deferred v1.6.1). Step-0 ready to build next. |

## Ready to plan (next)

_Empty. Calendar-binding moved to In flight after `/plan-feature` produced the folder. After calendar-binding step-0 builds, the next candidates are in the Vision section below._

## Designed (architecture set, larger design still needed)

| Item | Doc | Version | What's pending |
|---|---|---|---|
| Three-surface architecture (Context / Vandaag / Tijdlijn) | [ADR 0006](decisions/0006-three-surface-architecture.md) | Decision | Accepted 2026-06-01; data-model + UX shape resolved 2026-06-02. Tab label evolved three times same day (Verloop → Periodes → Context). Final order **Context / Vandaag / Tijdlijn** with Vandaag centre-positioned for thumb balance. See [features/verloop-and-episodes/](features/verloop-and-episodes/). |

## Vision (design session needed first)

Items here are coherent enough to name but need a deeper conversation about tradeoffs (cost, privacy, locality, scope) before any commitment.

| Item | Doc | Likely version |
|---|---|---|
| **Historical CSV backfill** — parse the user's 1.363-day Google Sheet export into `day_entries`. Domain parser is scoped; the import-driving UI + dedup-against-existing-days are not. Backlogged because new entries flow in via the app now, but trends + streak counter remain blank for everything pre-2026-05-28 until this lands. | [features/csv-import/](features/csv-import/) (parser plan) | v1.6 |
| Calendar-bound episodes (Shape B) — promote a recurring calendar series to an episode that auto-tracks it. Defer marker; trigger = v1.6 soak shows the user repeatedly linking many events to a single episode. | [features/calendar-binding/step-6-v1.6.1-calendar-bound-episodes.md](features/calendar-binding/step-6-v1.6.1-calendar-bound-episodes.md) | v1.6.1 |
| User-defined keyword exclusion rules — Settings → Kalenders → Regels. Trigger = v1.6 soak shows > 5 per-event exclusions/week with recognisable patterns. | sub-section in [features/calendar-binding/](features/calendar-binding/) §Future considerations | v1.6.x |
| Tag intelligence — LLM note-inference, correlation surfacing, merge/consolidate | [features/tag-intelligence/](features/tag-intelligence/) | v2 |
| Learned calendar suggestion rules — pattern-match `calendar_events.user_decision` to surface "suggest excluding this series" prompts. Trigger = v1.6.x soak data. | [features/calendar-binding/step-4-v2-learned-rules.md](features/calendar-binding/step-4-v2-learned-rules.md) | v2 |
| Second calendar provider (Outlook / Apple) — additional `CalendarProvider` implementations exercising the v1.6 interface. Trigger = user asks. | [features/calendar-binding/step-5-v2-second-provider.md](features/calendar-binding/step-5-v2-second-provider.md) | v2 |
| Garmin integration (continuous-stream layer on timeline) | not yet documented | v2 |
| Multi-user / per-user data scoping (schema migration: `user_owner` on `tags`, `day_entries`) | not yet documented | v2 |
| **Data export (CSV / JSON)** — promised on `/over` but **deferred until multi-user lands** (single-user, single-admin: Directus admin export is sufficient; the `binnenkort` stub in Settings remains aspirational). | _to be written_: `features/data-export/` | v2 (blocked on multi-user) |
| **Account deletion** — same `/over` promise; same deferral. Single-user means there's no "log out and leave" pressure; Directus admin handles deletion. | _to be written_: `features/account-deletion/` | v2 (blocked on multi-user) |
| Episode categories beyond v1.5: `project`, `patroon` | [features/verloop-and-episodes/](features/verloop-and-episodes/) §Out of scope | v2 |

## Shipped (recent)

| Item | Doc | When |
|---|---|---|
| **Tag merge** | [features/tag-merge/](features/tag-merge/) | 2026-06-03 (commits `36737f5..35b9421`; v1.5c — `mergeTag` SDK with combined source+target read + bulk-DELETE-then-bulk-PATCH junction rewrite + recount-from-truth + source hard-delete; `POST /api/tags/[id]/merge` route; `useTagManage.merge`; `TagMergeTargetPickerSheet` with internal confirm-mode; `TagFormSheet` integration with `tags` corpus threaded from `TagManagementSection`; 54 new vitest tests; prod smoke 11/11 against deployed frontend.) |
| **Tier 3 CHECK constraints (step-0b)** | [features/tag-merge/step-0b-check-constraints.md](features/tag-merge/step-0b-check-constraints.md) | 2026-06-03 (commit `063b609`; v1.5d — 7 CHECK constraints applied to prod: tag/episode category enums, `score BETWEEN 1 AND 10`, `sleep_hours BETWEEN 0 AND 24`, `episodes.end_date >= start_date`, `confidence BETWEEN 0 AND 1` on both junction tables. Reuses step-0's audit→apply→verify pattern; new `verifyCheckConstraints` lib joins pg_constraint + pg_class. Prod verifier now 56/56 green; constraint-enforcement smoke 6/6 — Directus surfaces PG 23514 on each violation.) |
| **DB integrity hardening (step-0)** | [features/tag-merge/step-0-junction-integrity.md](features/tag-merge/step-0-junction-integrity.md) | 2026-06-03 (commits `36737f5..2228f63`; 4 UNIQUE indexes — junction-pair composites on `day_entries_tags` + `project_entries_tags`, partial case-insensitive `(LOWER(label), category) WHERE archived_at IS NULL` on `tags` + `episodes`; new `pg`-backed `runSqlFile` + `queryPg` helpers; `verify-schema.mjs` extended with 6 FK `on_delete` assertions + 4 UNIQUE assertions; prod verifier 49/49 green; constraint-enforcement smoke 6/6.) |
| Tag management in Settings | [features/tag-management-settings/](features/tag-management-settings/) | 2026-06-03 (commit `b58433f` + 2 hotfixes `070b64c` / `b233c2d`; v1.5b — rename / recategorize / archive / un-archive / re-parent / hard-delete with confirm.) |
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
