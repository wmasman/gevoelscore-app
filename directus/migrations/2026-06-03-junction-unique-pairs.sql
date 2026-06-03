-- Step 0 / AC0.6 — junction-pair uniqueness.
--
-- Both M2M junctions store (foreign-key, tags_id) pairs. Without a UNIQUE
-- composite, duplicate junction rows can silently exist; the tag-merge
-- feature depends on this constraint being live so its bulk-delete-then-
-- bulk-patch ordering is BOTH semantically correct AND DB-enforced.
--
-- Idempotent via IF NOT EXISTS. Safe to re-run.

CREATE UNIQUE INDEX IF NOT EXISTS day_entries_tags_unique_pair
  ON day_entries_tags (day_entries_id, tags_id);

CREATE UNIQUE INDEX IF NOT EXISTS project_entries_tags_unique_pair
  ON project_entries_tags (project_entries_id, tags_id);
