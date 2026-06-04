-- Step 0 / calendar-binding v1.6 — UNIQUE, INDEX, and CHECK constraints
-- for the four new/migrated collections.
--
-- Directus' /collections + /fields API creates the tables and columns;
-- this file applies what the REST API can't:
--   - composite UNIQUE indexes
--   - non-unique performance indexes
--   - CHECK constraints
--
-- FK constraints are registered via Directus /relations API (see
-- setup-calendar-collections.mjs) so the admin UI handles them.
--
-- Idempotent via CREATE ... IF NOT EXISTS + DO blocks. Safe to re-run.

-- ─────────────────────────────────────────────────────────────────
-- UNIQUE composites (idempotent: CREATE UNIQUE INDEX IF NOT EXISTS)
-- ─────────────────────────────────────────────────────────────────

CREATE UNIQUE INDEX IF NOT EXISTS calendar_events_provider_event_unique
  ON calendar_events (connection_id, provider_event_id);

CREATE UNIQUE INDEX IF NOT EXISTS calendar_connections_user_provider_email_unique
  ON calendar_connections (user_id, provider, provider_account_email);

CREATE UNIQUE INDEX IF NOT EXISTS calendar_series_exclusions_unique
  ON calendar_series_exclusions (connection_id, recurrence_id);

CREATE UNIQUE INDEX IF NOT EXISTS cron_monitor_job_name_unique
  ON cron_monitor (job_name);

-- ─────────────────────────────────────────────────────────────────
-- Performance indexes (non-unique)
-- ─────────────────────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS calendar_events_connection_start_idx
  ON calendar_events (connection_id, start_at);

CREATE INDEX IF NOT EXISTS calendar_events_connection_recurrence_idx
  ON calendar_events (connection_id, recurrence_id);

-- ─────────────────────────────────────────────────────────────────
-- CHECK constraints (idempotent via pg_constraint pre-check)
-- ─────────────────────────────────────────────────────────────────

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'calendar_connections_status_check') THEN
    ALTER TABLE calendar_connections
      ADD CONSTRAINT calendar_connections_status_check
      CHECK (status IN ('active','disconnected','error'));
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'calendar_connections_provider_check') THEN
    ALTER TABLE calendar_connections
      ADD CONSTRAINT calendar_connections_provider_check
      CHECK (provider IN ('google'));
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'calendar_events_provider_check') THEN
    ALTER TABLE calendar_events
      ADD CONSTRAINT calendar_events_provider_check
      CHECK (provider IN ('google'));
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'calendar_events_user_decision_check') THEN
    ALTER TABLE calendar_events
      ADD CONSTRAINT calendar_events_user_decision_check
      CHECK (user_decision IN ('auto','user_included','user_excluded'));
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'calendar_events_end_after_start_check') THEN
    ALTER TABLE calendar_events
      ADD CONSTRAINT calendar_events_end_after_start_check
      CHECK (end_at >= start_at);
  END IF;

  -- Step-0 amendment 2026-06-04: status enum constraint
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'calendar_events_status_check') THEN
    ALTER TABLE calendar_events
      ADD CONSTRAINT calendar_events_status_check
      CHECK (status IN ('confirmed','tentative','cancelled'));
  END IF;
END $$;
