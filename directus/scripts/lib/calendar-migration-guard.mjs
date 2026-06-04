// Asserts the v1 calendar_events placeholder is empty before destructive
// migration to the v1.6 multi-provider shape. Refuses to run if rows exist.
//
// See docs/features/calendar-binding/step-0-data-model-and-provider.md
// AC0.17.
//
// Note: queryFn is injected so the function tests cleanly. In production,
// the caller passes queryPg from sql-migration.mjs.

export async function assertCalendarEventsEmpty(queryFn) {
  const rows = await queryFn('SELECT COUNT(*)::int AS count FROM calendar_events');

  if (!rows || rows.length === 0) {
    throw new Error(
      'calendar_events query returned no rows; expected one row with count',
    );
  }

  const rawCount = rows[0]?.count;
  if (rawCount === undefined || rawCount === null) {
    throw new Error(
      'calendar_events query returned a row without a count field',
    );
  }

  // PG COUNT() returns int8 which the pg driver may serialise as a
  // string or number depending on column-type config. Coerce to number
  // for the zero check.
  const count = Number(rawCount);
  if (Number.isNaN(count)) {
    throw new Error(`calendar_events count is not numeric: ${rawCount}`);
  }

  if (count !== 0) {
    throw new Error(
      `calendar_events not empty (${count} rows); refusing to migrate. ` +
        'Drop existing rows manually (admin UI) or design a backfill — out of scope here.',
    );
  }
}
