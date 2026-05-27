-- View: tag_correlations
--
-- Per-tag aggregate of how that tag correlates with the daily score.
-- This is the answer to "on days I logged X, what was my average score?"
-- precomputed for every tag.
--
-- Idempotent: CREATE OR REPLACE. View recomputes on every SELECT — no manual
-- refresh needed. For 1.363 rows + 83 tags the cost is trivial; if it grows
-- to hundreds of thousands of junction rows we may want a materialised view.
--
-- Note on STDDEV_POP vs STDDEV_SAMP: POP treats the days-with-tag as the
-- whole population (correct for "what's the spread of scores when I had
-- this tag?"). SAMP would be right if we were estimating a wider population
-- from a sample — we're not.

CREATE OR REPLACE VIEW tag_correlations AS
SELECT
  t.id                                       AS tag_id,
  t.label,
  t.category,
  t.parent_id                                AS tag_parent_id,
  COUNT(*)                                   AS day_count,
  AVG(d.score)::numeric(4, 2)                AS avg_score,
  STDDEV_POP(d.score)::numeric(4, 2)         AS stddev_score,
  MIN(d.score)                               AS min_score,
  MAX(d.score)                               AS max_score,
  MIN(d.date)                                AS first_seen,
  MAX(d.date)                                AS last_seen,
  -- only count user-confirmed or user-chosen rows separately, so we can tell
  -- "tag was seen on 200 days, user confirmed it on 12 of those"
  COUNT(*) FILTER (
    WHERE dt.source = 'user' OR dt.confirmed_at IS NOT NULL
  )                                          AS confirmed_day_count
FROM tags t
JOIN day_entries_tags dt ON dt.tags_id = t.id
JOIN day_entries d        ON d.id = dt.day_entries_id
GROUP BY t.id, t.label, t.category, t.parent_id;

COMMENT ON VIEW tag_correlations IS
  'Per-tag aggregate: day_count, avg_score, score spread, date range, confirmed-rows count. Read-only. Re-aggregates on every SELECT.';
