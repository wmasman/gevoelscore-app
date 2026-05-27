-- View: day_tags_flat
--
-- Denormalised one-row-per-(day, tag) projection of the day_entries_tags
-- M2M junction. Includes tag metadata (label, category, parent_id) and the
-- provenance columns (source, confidence, confirmed_at) so analysis queries
-- can filter "tags the user confirmed" vs. "auto-inferred from notes" in one
-- step instead of a 3-way JOIN.
--
-- Idempotent: CREATE OR REPLACE.

CREATE OR REPLACE VIEW day_tags_flat AS
SELECT
  d.id              AS day_entry_id,
  d.date,
  d.score,
  d.note,
  t.id              AS tag_id,
  t.label,
  t.category,
  t.parent_id       AS tag_parent_id,
  dt.source         AS tag_source,
  dt.confidence     AS tag_confidence,
  dt.confirmed_at   AS tag_confirmed_at,
  dt.sort           AS tag_sort
FROM day_entries d
JOIN day_entries_tags dt ON dt.day_entries_id = d.id
JOIN tags t              ON t.id = dt.tags_id;

COMMENT ON VIEW day_tags_flat IS
  'Denormalised day x tag rows. Read-only. Combines day_entries + day_entries_tags + tags so a single WHERE clause can filter by tag, category, source, or date.';
