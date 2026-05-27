-- View: daily_observations
--
-- Wide cross-source join keyed by date. One row per day_entries row, with
-- LEFT JOINs to passive-data sources (garmin, health, weather). LEFT means
-- a day_entry shows up even if no passive source has data for that date.
--
-- v1 reality: garmin/health/weather are empty placeholders — their JSON
-- `data` columns return null. The view still works; queries against it just
-- get nulls for those columns until v2 populates them.
--
-- Idempotent: CREATE OR REPLACE.
--
-- Apply with:
--   psql $env:DB_CONNECTION_STRING -f directus/scripts/views/01-daily-observations.sql
-- Or paste into the Neon SQL Editor.

CREATE OR REPLACE VIEW daily_observations AS
SELECT
  d.id            AS day_entry_id,
  d.date,
  d.score,
  d.note,
  d.sub_scores,
  d.sleep_hours,
  d.special_event,
  g.data          AS garmin_data,
  h.data          AS health_data,
  w.data          AS weather_data,
  d.created_at,
  d.updated_at
FROM day_entries d
LEFT JOIN garmin_daily  g ON g.date = d.date
LEFT JOIN health_daily  h ON h.date = d.date
LEFT JOIN weather_daily w ON w.date = d.date;

COMMENT ON VIEW daily_observations IS
  'Cross-source aggregate per local-date. Read-only. LEFT JOINs keep day_entries visible even when passive sources have no row for that date.';
