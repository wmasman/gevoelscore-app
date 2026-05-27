# Architecture docs — index

Where to look for what.

| Document | Purpose |
|----------|---------|
| [system-overview.md](system-overview.md) | High-level view: what runs where, what depends on what, the data path from a daily-entry tap to Postgres |
| [current-state.md](current-state.md) | **Living document** — concrete deployed resources (Fly app names, Neon project IDs, region, sizes). Update when infrastructure changes. |
| [data-model.md](data-model.md) | Source of truth for every entity (DayEntry, Tag, Project, ...). The Directus schema is a downstream copy of this. |
| [directus-setup.md](directus-setup.md) | Provisioning runbook — how the live infra was built. Mostly historical now (Phase 1 done); Phases 2–4 are the schema/permissions/CORS automation, which is captured in [`directus/scripts/`](../../directus/scripts/). |
| [directus-schema-management.md](directus-schema-management.md) | **Canonical approach** for ongoing schema changes. The three lessons from the TVO project (bootstrap is one-time; `schema apply` can't bootstrap empty DBs; **the one-POST rule**). |

For operational stuff — credentials, scripts inventory, rotation procedures, runbooks for common operations — see [`docs/operations/`](../operations/).

For architectural decisions and the reasoning behind them, see [`docs/decisions/`](../decisions/).
