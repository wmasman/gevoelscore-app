# ADR 0007: Self-hosted Postgres on Fly; machines scale-to-suspend

- **Status**: Accepted (implemented 2026-07-14)
- **Date**: 2026-07-14
- **Builds on**: [ADR 0002](0002-pwa-with-directus-backend.md) (Directus-backed stack), [ADR 0003](0003-directus-fly-infra-setup.md) (Fly infra; Neon Postgres per its 2026-05-27 amendment)
- **Amends**: ADR 0003 — Postgres provider and the always-on machine commitment
- **Deciders**: Willem Masman (author), Claude (AI collaborator)

## Context

On 2026-07-10 Neon cut off all query execution: the free-tier compute quota was exhausted mid-month. Every Directus request returned 500, `/server/health` returned 503, and the app was dark until 2026-07-14 — four days without daily logging, which for a daily tracker means holes in the data record, not just downtime. Recovery required upgrading the Neon org to a paid plan.

The subsequent compute audit found the cost had nothing to do with data volume (1-2 entries/day; 46 MB database). It was **standby economics**:

- The Neon endpoint was sized **min 1 CU / max 9 CU** — 4x the smallest compute for a database that fits in RAM twenty times over. ~110 compute-hours burned in July 1-10 (~11 active hours/day at ~1 CU).
- Every touch (app open, cron ping, script run) cost a query burst plus the 300-second suspend tail — ~7-8 minutes of billed compute per wake. Wake sources: the user's own app usage (dominant), the 6-hourly GH watchdog, the daily calendar sync, dev/test runs.
- Neon's own suspend mechanics were healthy (verified empirically: the endpoint suspended ~5-7 min after the last query; Directus's pool did not pin it). The mismatch was structural: serverless-Postgres pricing is built for variable multi-tenant load, not a single-user app with a tiny always-warm working set.
- A shared-org wrinkle: the project lived in the old TVO Neon org, so TVO's final-days usage (deleted 2026-07-04) plausibly ate into the same July quota.

Resizing to 0.25-1 CU (done 2026-07-14) cut the burn ~4x, but the free tier's failure mode remains a hard mid-month cliff, and the paid plan (~$19/mo) buys quota headroom a single-user app doesn't need.

Separately, both Fly machines ran 24/7 (`auto_stop_machines` off, `min_machines_running = 1`) — a commitment made in ADR 0003 when sessions lived in memory and a restart logged the user out. ADR 0005 moved sessions into Directus, removing that constraint.

## Options considered

### Option A — stay on Neon paid (~$19/mo)

No cliff, no migration. But pays for multi-tenant quota headroom a 46 MB single-user DB never uses, and keeps the CU/suspend-window/quota mental model as a permanent operational concern.

### Option B — Neon free tier + usage alarm

$0 at the current (post-resize) burn projection of ~85 CU-h/month, with a watchdog-driven quota alert. Rejected as the primary plan: the projection was tight against the allowance, the cliff failure mode lands on the product's core value (gapless daily logging), and July proved the cliff is real.

### Option C — self-hosted Postgres on Fly (chosen)

A single-node postgres-flex app in the existing org. Flat ~$2-3/mo, no quotas, no compute-hours, no cliff. Data moves onto infrastructure already trusted with the uploads volume and reduces the third-party surface (Neon drops out as a processor of Art. 9 health data — see [gdpr-art9.md](../compliance/gdpr-art9.md)). The new obligation is owning backups.

### Option D — SQLite on the existing volume

The theoretical minimum for one user, but the repo has real Postgres-specific surface (partial unique indexes, CHECK constraints, views, `sql-migration.mjs`) — a porting project, not a swap. Rejected on effort/risk; pg_dump/restore preserves everything as-is.

## Decision

1. **Database**: Fly Postgres app `gevoelscore-pg` (postgres-flex, PostgreSQL 18), single node, `ams`, shared-cpu-1x 256MB, 2 GB encrypted volume, org-internal only (no public address). Directus connects via `gevoelscore-pg.flycast:5432`, database `gevoelscore`. Migrated 2026-07-14 by pg_dump (PG18 client against Neon's PG17 server) and restore on the new machine; verified 45 tables / 24,466 rows exact match against a pre-migration baseline, plus health, live reads, and the full auth smoke.
2. **Machines sleep when idle**: `auto_stop_machines = 'suspend'`, `min_machines_running = 0` on both frontend and backend. Suspend (memory snapshot) resumes in ~1s; verified cold-chain from both machines suspended: frontend first byte ~1.4s, full login → read → logout smoke in ~2.6s — comfortably inside the sub-10-second logging-flow budget. `gevoelscore-pg` stays always-on (it is the ~$2 flat-cost machine, and postgres-flex/repmgr tolerates stopping poorly).
3. **Two load-bearing config details** (both bit during implementation):
   - The frontend's `DIRECTUS_URL` must be the **public hostname**, not `gevoelscore-backend.internal` — `.internal` DNS bypasses the Fly proxy, so a suspended backend would never be woken.
   - The backend needs `DB_POOL__MIN = "0"` — Knex's default pool floor of 2 pins connections that freeze during suspend and are dead on resume, 500-ing the first requests after wake. With a zero floor the pool drains during the idle minutes that precede any suspend, so the machine wakes into a clean pool.
4. **Backups are now ours**: Fly automatic daily volume snapshots (retention raised to 14 days), the pre-migration dump retained on the volume as day-0, manual `pg_dump` to the volume before risky migrations. Procedures live in the operations runbooks.

## Consequences

### Positive

- Flat, quota-free cost: DB ~$2-3/mo; machines billed only while awake. Realistic total ~$3-6/mo, and the July outage class (mid-month usage cliff) is structurally impossible.
- Health data leaves Neon; one fewer processor, private-network-only database.
- Local SQL tooling keeps working (`fly proxy 15432:5432 -a gevoelscore-pg`; `DATABASE_URL` in `.env.local` points at the proxy).

### Negative

- Backup discipline is now a first-class operational duty — Neon's PITR/branching is gone (its 6-hour history retention on the free plan was thin anyway). Volume snapshots + dumps must actually be verified occasionally.
- Single-node Postgres: a volume loss between snapshots loses up to a day. Accepted for a single-user app whose entries can be reconstructed from memory for a day.
- First interaction after idle carries ~1.5-2.5s wake latency. Accepted explicitly ("some lag is not important for me").

### Migration cost if revisited

pg_dump/restore back to any managed Postgres is the same ~15-minute procedure this migration used. If multi-user ever lands (backers page), managed Postgres becomes attractive again — revisit then.

## When to revisit

- Multi-user or offline-sync work starts (v2 roadmap) — managed Postgres and PITR re-earn their price.
- The suspended-machine wake latency starts violating the sub-10s logging flow in practice.
- Backup verification reveals gaps (then consider WAL archiving to object storage, e.g. postgres-flex's Tigris option — deliberately skipped now to avoid adding a third-party holding full WAL of health data without an explicit decision).

## References

- Neon quota outage + compute audit + migration: session 2026-07-14 (Claude Code)
- [ADR 0003 amendment 2026-05-27](0003-directus-fly-infra-setup.md#amendment-2026-05-27-postgres-provider-switched-to-neon) — the decision this supersedes
- [docs/operations/runbooks/rotate-credentials.md](../operations/runbooks/rotate-credentials.md) — updated DB credential + recovery procedures
