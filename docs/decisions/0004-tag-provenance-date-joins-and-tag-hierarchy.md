# ADR 0004: Tag provenance, date-joined cross-source queries, and tag hierarchy

- **Status**: Accepted
- **Date**: 2026-05-27
- **Builds on**: [ADR 0002](0002-pwa-with-directus-backend.md) (stack), [ADR 0003](0003-directus-fly-infra-setup.md) (infra)
- **Deciders**: Willem Masman (author), Claude (AI collaborator)

## Context

After the M2M upgrade for `day_entries × tags` (2026-05-27 morning), a database-expert review surfaced four weaknesses in the v1 schema that affected the user's three explicit goals: (1) easy semantic tagging from notes, (2) clean expansion into Garmin / Apple Health / Calendar / Weather data sources, and (3) robust aggregation and cross-reference queries.

The weaknesses:

1. **Tag provenance was missing.** The 1,338 junction rows imported by `import-real-history.mjs` were indistinguishable from any tag a user might later choose by hand. Re-running pattern inference would clobber user choices.
2. **JSON-array foreign keys remained on `day_entries`.** `project_entry_ids` and `calendar_event_ids` repeated the anti-pattern that the morning's M2M upgrade had just removed for tags, and `project_entries.tag_ids` still held the old JSON-array shape.
3. **Tag schema was strictly flat.** `migraine` and `hoofdpijn` were siblings; no way to walk "all headache-like days" without an OR-list of labels.
4. **No documented cross-source query surface.** Aggregating `day_entries × garmin_daily × health_daily × weather_daily × tags` was possible only by hand-rolling joins per query.

This ADR locks the choices made to address these four weaknesses.

## Options considered

### Option set A — tag provenance

| Option | Pros | Cons |
|---|---|---|
| **A1. Add `source`/`confidence`/`confirmed_at` columns to `day_entries_tags`** (chosen) | Minimal schema change. Backfill-safe. Distinguishes user choice from inference. Enables "show unconfirmed tags" UI. | Three nullable columns per junction row (~24 bytes overhead per row × 1,338 rows ≈ trivial). |
| A2. Separate `tag_inferences` audit table | Cleaner separation of facts vs. inferences. Full history of inference runs. | Doubles the write volume per tag. Doesn't solve the "is this tag user-confirmed?" query without a join. Premature for a single-user app. |
| A3. Drop the question — re-run the regex every time we display tags, never persist inferred ones | No schema change. | Defeats the purpose of the junction. Forces every read to re-execute the pattern library. Loses the ability for the user to override an inference. |

**Chosen: A1.** Simplest path that meets all four goals: distinguishes user from inferred, supports confidence weighting, allows the "user confirmed an inferred tag" workflow, and keeps a single junction row per (day, tag).

### Option set B — JSON-array foreign keys → drop or convert?

| Option | Pros | Cons |
|---|---|---|
| **B1. Drop `day_entries.project_entry_ids` + `calendar_event_ids` entirely; join by `date`** (chosen) | One join key (`date`) across every passive source. Passive data (Garmin/calendar) can arrive before a `day_entry` exists. No id-arrays to keep in sync. Same join pattern works for `garmin_daily`, `health_daily`, `weather_daily`. | Loses the explicit "this day_entry has these specific events" link. Mitigated by: `date` is the natural identity anyway, and the alternative is duplicating ids in two places. |
| B2. Convert to 1:N FKs on the child collections (`project_entries.day_entry_id`, `calendar_events.day_entry_id`) | Explicit FK with CASCADE. Directus UI shows the relation. | Forces day_entry to exist before child rows can be persisted — bad for passive data sources that may arrive before the user logs that day. Nullable FK + date-join works, but adds redundancy with the `date` column. |
| B3. Keep the JSON arrays | No work. | Same anti-pattern we just removed for tags — synchronisation hazard, no referential integrity, hostile to SQL aggregation. |

**Chosen: B1.** `date` is the natural join key for every daily-grain entity. The child collections already carry their own `date`. Adding an id-array on `day_entries` is redundant; adding an FK on the child couples persist-order to user behaviour. Drop the redundancy.

For `project_entries × tags`, the same M2M shape as `day_entries × tags` is the correct answer (chosen).

### Option set C — tag categories: flat enum vs. tag_categories table vs. parent_id

| Option | Pros | Cons |
|---|---|---|
| **C1. Keep `category` enum flat + add `tags.parent_id` self-FK for hierarchy** (chosen) | Type-safe in TS (`'mentaal' \| 'fysiek' \| …`). Categories are locked-by-UX (chip rows on the daily screen). Hierarchy handles the only real use case (`migraine` → `hoofdpijn`). Per-category metadata (color, icon) lives in code where it belongs. | parent_id adds a self-join surface; cycle prevention is a domain-layer concern. |
| C2. Move categories to a `tag_categories(id, name, color, icon, sort_order)` table | Per-category metadata in DB. User-creatable categories. | Categories aren't supposed to be user-creatable (UX commitment). DB color values mean a deploy-equivalent change to update visuals. Extra JOIN on every tag read. |
| C3. Make categories themselves Tag rows (tags-as-tree with `parent_id = null` at the cluster root) | One table, recursive. Elegant in theory. | Conflates "the cluster" with "a tag in the cluster." `category` field on Tag becomes redundant or contradictory. Bad TS ergonomics. |

**Chosen: C1.** The 6 v1 clusters (`mentaal | fysiek | overall | activiteit | gebeurtenis | interventie`, plus the specials `project | custom`) are stable, deliberate, and locked by the daily-screen design. Hierarchy is the only realistic schema evolution, and `parent_id` covers it.

### Option set D — cross-source query surface

| Option | Pros | Cons |
|---|---|---|
| **D1. Postgres views (`daily_observations`, `day_tags_flat`, `tag_correlations`) — read-only, idempotent (`CREATE OR REPLACE`)** (chosen) | One-liner queries for common cross-source aggregations. Views are invisible to Directus until explicitly registered. Pure SQL — no application code to maintain. Free to evolve via re-CREATE. | Apply step is out-of-band (psql or Neon Console). Materialised views would be faster at scale; non-materialised is fine for 1,363 rows + 83 tags. |
| D2. Generic `observations(date, source, metric, value)` EAV table | Infinitely extensible. | Loses type safety. Every query needs schema knowledge in the WHERE clause. 95% of queries want one named column at a time. |
| D3. Application-layer aggregation in `src/lib/api/` | All queries in TypeScript. | Re-implements joins the database is built for. Couples query patterns to the application code's release cycle. |
| D4. Defer entirely until a UI consumer exists | No work now. | The user's stated goal includes "robust and queryable system… aggregate cross-reference" — that's a now requirement, not a future one. |

**Chosen: D1.** Views are the right primitive for read-only aggregates that exist alongside the OLTP shape. They don't change the Directus collections or the application code. They're easy to re-apply via `CREATE OR REPLACE`. When the UI lands, registering a view as a read-only collection in Directus is a one-time admin-UI step.

## Decision

### Tag provenance

`day_entries_tags` and `project_entries_tags` both carry:

```sql
source        VARCHAR(20) NULL  -- 'user' | 'note_pattern' | 'csv_import' | 'inferred'
confidence    REAL        NULL  -- 0..1; NULL when source='user'
confirmed_at  TIMESTAMPTZ NULL  -- set when the user reviews and accepts an inferred tag
```

NULL `source` is treated as legacy / pre-migration; backfilled to `'note_pattern'` for the existing 1,338 rows. New rows must set `source` explicitly.

### Date-join over id-array

The following JSON-array fields are **removed** from the schema:

- `day_entries.project_entry_ids`
- `day_entries.calendar_event_ids`
- `project_entries.tag_ids`

Cross-collection joins now happen by `date`:

```sql
SELECT *
FROM day_entries d
LEFT JOIN project_entries pe ON pe.date = d.date
LEFT JOIN calendar_events  ce ON ce.date = d.date
LEFT JOIN garmin_daily     g  ON g.date = d.date;
```

`project_entries × tags` gains the same M2M shape as `day_entries × tags`, with the same provenance columns. Schema is ready; no data populated yet (project_entries empty in v1).

### Tag hierarchy

`tags.parent_id` (`UUID NULL`, self-FK, `ON DELETE SET NULL`) is added. Convention is to keep parent and child in the same `category`; this is not enforced at the DB layer but is enforced in the domain validator (to be added when the UI uses hierarchy).

Per-category metadata (color, icon, display label, sort order) lives in `src/lib/domain/tag-category-meta.ts` (to be created when the UI lands), not in the database.

### Query views

Three views, created via `CREATE OR REPLACE` so re-applying is safe:

| View | Purpose |
|---|---|
| `daily_observations` | Wide LEFT JOIN of `day_entries × garmin_daily × health_daily × weather_daily` by `date`. Useful for v2 cross-source analysis. |
| `day_tags_flat` | Denormalised `(day, tag)` rows with provenance + tag metadata. Single-table filtering by tag, category, source, or date. |
| `tag_correlations` | Per-tag aggregate: `day_count`, `avg_score`, `stddev_score`, `min/max_score`, `first_seen`, `last_seen`, `confirmed_day_count`. |

Source-of-truth files in [`directus/scripts/views/`](../../directus/scripts/views/). Apply path: paste into Neon Console SQL editor, or `psql -f` if available.

## Commitments

| Layer | Commitment |
|---|---|
| Cross-collection joins | Use `date` as the join key. No id-arrays on `day_entries`. |
| Tag attribution | Every junction row records its `source`. Pattern inference may overwrite only rows where `source != 'user'` and `confirmed_at IS NULL`. |
| Tag categories | Stay a flat enum on `Tag`. Hierarchy via `parent_id` only. New categories require an ADR amendment. |
| Per-category metadata | Lives in `src/lib/domain/tag-category-meta.ts`. Not in the database. |
| Query views | Postgres views for read-only aggregation. Application code prefers the view over reconstructing the join. |
| View evolution | `CREATE OR REPLACE`. Re-applying is the migration. |
| Verify-schema | The verification list grows with every new typed column. Current count: 29/29. |

## Consequences

### Positive

- **Re-running pattern inference is now safe.** It can be written to update only rows where `source != 'user' AND confirmed_at IS NULL`. User choices survive.
- **One join key (`date`) for every passive data source.** Garmin / Apple Health / Calendar / Weather all plug into the same join pattern. No special-casing per source.
- **Tag hierarchy is in place without forcing it to be used.** `parent_id = NULL` for all 83 v1 tags. When the UI wants `migraine → hoofdpijn`, the column is there.
- **Cross-source queries are one-liners.** `SELECT * FROM tag_correlations ORDER BY avg_score` instead of a hand-built triple-JOIN.
- **Domain layer untouched.** 254/254 tests still pass — the schema changes are below the domain boundary.

### Negative

- **Provenance columns add three NULL columns per junction row.** Negligible at v1 scale (~24 bytes × 1,338 = ~32 KB). Will scale to ~250 KB at 10× growth — still negligible.
- **Views are applied out-of-band.** No automated `node directus/scripts/apply-views.mjs` because the dep-free constraint forbids a `pg` client. Mitigation: SQL files are short and `CREATE OR REPLACE` is idempotent — paste once into Neon Console.
- **`parent_id` cycle prevention is a domain concern, not a DB constraint.** A direct `parent_id = self.id` is forbidden by the validator; deeper cycles (A → B → A) are not enforced at the DB layer. Mitigation: the use case (sub-tag under a cluster head) doesn't require deep chains; add a `WITH RECURSIVE` cycle check in the validator if cycles ever happen in practice.

### Migration cost if revisited

- **Removing provenance**: trivial — drop the three columns. Lose the user/inference distinction.
- **Re-introducing id-arrays**: a backwards step; would require a backfill from the date-joined views.
- **Moving to a `tag_categories` table**: ~1 hour. Add the table, FK from `tags`, backfill from the enum values, drop the enum constraint.
- **Materialised views**: when the row count crosses ~100,000 junctions, swap `CREATE OR REPLACE VIEW` for `CREATE MATERIALIZED VIEW` + a `REFRESH MATERIALIZED VIEW CONCURRENTLY` cron.

## When to revisit

Revisit this ADR if:

- A second user joins (changes the "categories are locked by UX" assumption — they may want their own clusters).
- The tag library grows past ~500 tags (flat category enum starts to feel tight).
- Pattern inference accuracy drops below ~75% (may want a separate `tag_inferences` table to track per-run quality).
- Cross-source queries become slow (move to materialised views).
- A new data source doesn't fit the daily-grain model (e.g., per-event heart-rate spikes from Garmin) — date-join breaks down for sub-day events.

## What's NOT in this ADR (intentionally deferred)

- **Domain-layer validators for `parent_id` (cycle prevention, same-category enforcement)** — added when the UI first uses hierarchy. The DB schema is ready; the validator is pure-TS work.
- **Registering views as Directus collections** — manual admin-UI step, done when a screen first queries a view.
- **Materialised view migration** — only if/when needed.
- **Sub-day event tables** (`garmin_events`, `weather_events`) — when v2 reveals a real need; daily aggregates carry v1/v1.5.

## References

- [ADR 0002](0002-pwa-with-directus-backend.md) — stack choice
- [ADR 0003](0003-directus-fly-infra-setup.md) — infrastructure commitments
- [docs/architecture/data-model.md](../architecture/data-model.md) — entity-level types (kept in sync with this ADR)
- [docs/architecture/queries-and-views.md](../architecture/queries-and-views.md) — how to query the database
- [docs/architecture/directus-schema-management.md](../architecture/directus-schema-management.md) — canonical M2M-with-provenance pattern
- [directus/scripts/views/](../../directus/scripts/views/) — view definitions
- [directus/scripts/add-tag-provenance.mjs](../../directus/scripts/add-tag-provenance.mjs), [flatten-day-entry-json-arrays.mjs](../../directus/scripts/flatten-day-entry-json-arrays.mjs), [add-tag-hierarchy.mjs](../../directus/scripts/add-tag-hierarchy.mjs) — the one-time migrations
