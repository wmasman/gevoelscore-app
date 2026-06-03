-- Step 0b — Tier 3 CHECK constraints. Defense-in-depth: the app-layer
-- domain validators already enforce these ranges, but a buggy script,
-- admin-UI tap, or future migration could bypass them. With these in
-- place, PostgreSQL rejects nonsense values (PG error 23514).
--
-- Idempotent via DO blocks + IF NOT EXISTS in pg_constraint lookup.
-- Safe to re-run.
--
-- The pre-flight audit (find-check-violations.mjs) MUST report 0
-- violations before this migration is applied — otherwise ADD CONSTRAINT
-- fails for the violating rows.

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'tags_category_check') THEN
    ALTER TABLE tags
      ADD CONSTRAINT tags_category_check
      CHECK (category IN ('mentaal','fysiek','overall','activiteit','gebeurtenis','interventie','project','custom'));
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'episodes_category_check') THEN
    ALTER TABLE episodes
      ADD CONSTRAINT episodes_category_check
      CHECK (category IN ('interventie','levensgebeurtenis'));
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'day_entries_score_check') THEN
    ALTER TABLE day_entries
      ADD CONSTRAINT day_entries_score_check
      CHECK (score BETWEEN 1 AND 10);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'day_entries_sleep_hours_check') THEN
    ALTER TABLE day_entries
      ADD CONSTRAINT day_entries_sleep_hours_check
      CHECK (sleep_hours IS NULL OR sleep_hours BETWEEN 0 AND 24);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'episodes_date_order_check') THEN
    ALTER TABLE episodes
      ADD CONSTRAINT episodes_date_order_check
      CHECK (end_date IS NULL OR end_date >= start_date);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'day_entries_tags_confidence_check') THEN
    ALTER TABLE day_entries_tags
      ADD CONSTRAINT day_entries_tags_confidence_check
      CHECK (confidence IS NULL OR confidence BETWEEN 0 AND 1);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'project_entries_tags_confidence_check') THEN
    ALTER TABLE project_entries_tags
      ADD CONSTRAINT project_entries_tags_confidence_check
      CHECK (confidence IS NULL OR confidence BETWEEN 0 AND 1);
  END IF;
END $$;
