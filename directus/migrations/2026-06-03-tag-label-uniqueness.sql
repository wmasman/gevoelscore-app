-- Step 0 / AC0.7 — case-insensitive label uniqueness within category,
-- scoped to non-archived rows.
--
-- Prevents the duplicate-tag pressure that the tag-merge feature exists
-- to clean up: a future inline-tag-creation race or buggy retry cannot
-- create "hoofdpijn" + "Hoofdpijn" as separate fysiek tags.
--
-- Partial (WHERE archived_at IS NULL) so archive-then-create works: a
-- live tag can be archived and then a new tag with the same label can be
-- created without colliding with the archived ghost.
--
-- LOWER(label) makes the constraint case-insensitive.
--
-- Idempotent via IF NOT EXISTS.

CREATE UNIQUE INDEX IF NOT EXISTS tags_label_category_active_unique
  ON tags (LOWER(label), category)
  WHERE archived_at IS NULL;

CREATE UNIQUE INDEX IF NOT EXISTS episodes_label_category_active_unique
  ON episodes (LOWER(label), category)
  WHERE archived_at IS NULL;
