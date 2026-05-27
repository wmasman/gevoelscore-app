# Queries and views

How to read the database for aggregation, cross-reference, and pattern analysis. The OLTP shape (`day_entries`, `tags`, junctions) is optimised for writes; this document covers the read-side surface.

For the write path, see [data-model.md](data-model.md). For the design choices behind the query surface, see [ADR 0004](../decisions/0004-tag-provenance-date-joins-and-tag-hierarchy.md).

---

## Three ways to read the database

Pick the lowest layer that answers the question.

| Layer | Use when | Tooling |
|---|---|---|
| **Directus REST API** | The screen needs entities with their immediate relations (`day_entry` + its `tags`). User auth applies. | `@directus/sdk`, `/items/{collection}?fields=*,tags.tags_id.*` |
| **Postgres views** | The screen needs an aggregate, a cross-source join, or a denormalised projection. No user auth — bypass Directus. | psql, Neon Console, or register the view as a read-only collection in Directus |
| **Raw SQL** | One-off analysis, debugging, ad-hoc exploration. | psql or Neon Console |

The views layer is the middle ground: it captures repeated query patterns once, lives in Postgres (not in application code), and is read-only by definition.

---

## The join principle: everything joins by `date`

Every daily-grain entity carries its own `date` column. There are no id-arrays linking `day_entries` to `project_entries` / `calendar_events` / `garmin_daily` / `health_daily` / `weather_daily`. The join key is always `date`.

```sql
-- The canonical cross-source query
SELECT *
FROM day_entries d
LEFT JOIN project_entries pe ON pe.date = d.date
LEFT JOIN calendar_events  ce ON ce.date = d.date
LEFT JOIN garmin_daily     g  ON g.date = d.date
LEFT JOIN health_daily     h  ON h.date = d.date
LEFT JOIN weather_daily    w  ON w.date = d.date
WHERE d.date BETWEEN '2026-05-01' AND '2026-05-27';
```

`LEFT JOIN` because passive data sources can have a row when `day_entries` doesn't (the user forgot to log), and vice versa. Inner joins drop those rows; for v1 reality (1,363 day_entries, 0 passive rows), `LEFT JOIN` is mandatory.

`date` is also the natural identity for `day_entries` (UNIQUE constraint, see [data-model.md](data-model.md)) and for the v2 source tables. No domain code interprets `Date` objects — strings only.

---

## Tag provenance — read the junction, not just the tag

Every row in `day_entries_tags` and `project_entries_tags` carries provenance:

| Column | Type | Meaning |
|---|---|---|
| `source` | `'user' \| 'note_pattern' \| 'csv_import' \| 'inferred' \| null` | Where this junction row came from. `null` = legacy (pre-2026-05-27 migration). |
| `confidence` | `real null` | 0..1. `null` when `source='user'` (full confidence by definition). |
| `confirmed_at` | `timestamptz null` | Set when the user reviews an inferred tag and accepts it. |

This is what lets re-running pattern inference be safe: an inference run can update only the rows where `source != 'user' AND confirmed_at IS NULL`. User choices are never overwritten.

```sql
-- Tags the user confirmed (either directly chose or accepted)
SELECT * FROM day_entries_tags
WHERE source = 'user' OR confirmed_at IS NOT NULL;

-- Tags pending review (auto-inferred, not yet user-confirmed)
SELECT * FROM day_entries_tags
WHERE source IN ('note_pattern', 'csv_import', 'inferred')
  AND confirmed_at IS NULL;
```

---

## Tag hierarchy — walk `parent_id`

`tags.parent_id` is a nullable self-FK. Convention: parent and child share the same `category`. NULL parent = top-level tag.

```sql
-- Direct children of a given tag
SELECT * FROM tags WHERE parent_id = '<uuid>';

-- All descendants (recursive)
WITH RECURSIVE tag_tree AS (
  SELECT id, label, category, parent_id, 0 AS depth
  FROM tags WHERE id = '<root-uuid>'
  UNION ALL
  SELECT t.id, t.label, t.category, t.parent_id, tt.depth + 1
  FROM tags t
  JOIN tag_tree tt ON t.parent_id = tt.id
)
SELECT * FROM tag_tree;
```

`ON DELETE SET NULL` — deleting a parent makes children orphans (top-level), not deletes them.

`parent_id` is `NULL` for all 83 v1 tags. The column is schema-ready; the convention emerges when the UI introduces sub-tags.

---

## The three Postgres views

Source-of-truth SQL: [`directus/scripts/views/`](../../directus/scripts/views/). All three are `CREATE OR REPLACE` — re-applying is the migration.

### `daily_observations` — wide cross-source projection

Joins `day_entries` LEFT to every v2 passive source by `date`. One row per `day_entry`, with `garmin_data` / `health_data` / `weather_data` as JSON columns (current v2 placeholder shape).

```sql
SELECT day_entry_id, date, score, note, garmin_data
FROM daily_observations
WHERE date >= CURRENT_DATE - INTERVAL '30 days';
```

In v1, the `*_data` columns are always `NULL` — the placeholder tables are empty. The view's shape is ready for v2 without re-creation.

### `day_tags_flat` — denormalised day × tag rows

One row per `(day, tag)` junction, joined to `day_entries` (for score/note) and `tags` (for label/category/parent_id), plus the junction's provenance.

```sql
-- All "fysiek" tag observations in May 2026
SELECT date, score, label, tag_source
FROM day_tags_flat
WHERE category = 'fysiek'
  AND date BETWEEN '2026-05-01' AND '2026-05-31'
ORDER BY date, label;

-- Days where the user confirmed at least one inferred tag
SELECT DISTINCT date
FROM day_tags_flat
WHERE tag_confirmed_at IS NOT NULL;
```

### `tag_correlations` — per-tag score aggregates

One row per tag with: `day_count`, `avg_score`, `stddev_score`, `min/max_score`, `first_seen`, `last_seen`, `confirmed_day_count`.

```sql
-- Top 10 tags by impact (lowest avg_score among tags with enough days)
SELECT label, category, day_count, avg_score, stddev_score
FROM tag_correlations
WHERE day_count >= 20
ORDER BY avg_score ASC
LIMIT 10;
```

The view recomputes on every SELECT. At v1 scale (1,338 junction rows × 83 tags) the cost is ~30–40 ms. If the row count crosses ~100k junctions, swap to a materialised view with a periodic `REFRESH` — see ADR 0004's "Migration cost if revisited."

---

## Applying or updating views

1. Edit the SQL in [`directus/scripts/views/*.sql`](../../directus/scripts/views/).
2. Apply via one of:
   - **Neon Console** (`console.neon.tech` → project → SQL editor) — paste and run. Works without local tooling.
   - **psql**: `psql $env:DB_CONNECTION_STRING -f directus/scripts/views/01-daily-observations.sql` (requires psql installed; the dep-free constraint on `directus/scripts/` rules out a Node-based applier).
3. (Optional) Register the view as a Directus read-only collection: admin UI → Settings → Data Model → Add Collection from Database. This makes the view queryable via `/items/<view_name>` with the frontend role's permissions applying.

Re-applying after edits is idempotent (`CREATE OR REPLACE`). No DROP needed.

---

## When NOT to use a view

- **Single-entity reads with their immediate relations** — use the Directus SDK. The REST API does field expansion (`?fields=*,tags.tags_id.*`) cleanly.
- **Mutations** — views are read-only. All writes go through Directus, where role-based permissions apply.
- **User-scoped filters** — views ignore Directus's permission layer. Until v1 stays single-user, this is fine; if a second user is ever added, queries against views need explicit user-filter predicates and the Directus registration becomes essential for permissions to apply.

---

## What's NOT covered by views (yet)

These query patterns don't have a view today; revisit if they recur:

- **Recent-missed-days panel** — "show me the days in the last 14 where I didn't log." A `LEFT JOIN` against `generate_series(CURRENT_DATE - 13, CURRENT_DATE, '1 day')` is one line in a query; not view-worthy until a screen needs it.
- **Tag co-occurrence matrix** — "when I tag `hoofdpijn`, what else do I tag?" Useful when sample sizes get bigger. Add as `tag_cooccurrence` view when the UI surfaces it.
- **Project-entry rollups** — empty in v1; when v1.5 projects ship, mirror the `tag_correlations` pattern.
- **Sub-day event aggregation** (Garmin spikes, weather changes) — not a daily-grain shape; would need a different table and view design when v2 introduces sub-day data.

---

## References

- [ADR 0004](../decisions/0004-tag-provenance-date-joins-and-tag-hierarchy.md) — design choices behind this query surface
- [data-model.md](data-model.md) — entity definitions
- [directus-schema-management.md](directus-schema-management.md) — canonical M2M-with-provenance pattern (matches what views project over)
- [directus/scripts/views/](../../directus/scripts/views/) — view definitions
- [docs/operations/scripts.md](../operations/scripts.md) — operational guide for applying views
