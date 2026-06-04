// Pure helpers for rendering CalendarEvent display values in Dutch.
// Kept domain-side so the component layer stays presentational.

const DUTCH_DAYS = [
  'zondag',
  'maandag',
  'dinsdag',
  'woensdag',
  'donderdag',
  'vrijdag',
  'zaterdag',
];
const DUTCH_MONTHS = [
  'januari',
  'februari',
  'maart',
  'april',
  'mei',
  'juni',
  'juli',
  'augustus',
  'september',
  'oktober',
  'november',
  'december',
];

/** Format a Date as "donderdag 4 juni 2026" in Europe/Amsterdam local time. */
export function formatDutchDate(d: Date): string {
  // We don't have timezone APIs in jsdom; use the browser's local time
  // (production runs in the user's tz). For v1.6 single-user app in NL
  // this is Europe/Amsterdam. v2 multi-user will need a per-user tz.
  const day = DUTCH_DAYS[d.getDay()];
  const date = d.getDate();
  const month = DUTCH_MONTHS[d.getMonth()];
  const year = d.getFullYear();
  return `${day} ${date} ${month} ${year}`;
}

/** Format a Date as "HH:mm" in local time. */
export function formatDutchTime(d: Date): string {
  const h = String(d.getHours()).padStart(2, '0');
  const m = String(d.getMinutes()).padStart(2, '0');
  return `${h}:${m}`;
}

/**
 * Format the event's datetime block:
 *  - All-day: "donderdag 4 juni 2026"
 *  - Timed:   "donderdag 4 juni 2026, 10:00 – 11:00"  (en-dash, not em-dash)
 *  - Multi-day timed: "donderdag 4 juni 2026, 10:00 – vrijdag 5 juni 2026, 09:00"
 */
export function formatEventDateTime(
  startAt: Date,
  endAt: Date,
  allDay: boolean,
): string {
  if (allDay) {
    // All-day events typically end the next local-midnight, so display
    // just the start date.
    return formatDutchDate(startAt);
  }
  const startDate = formatDutchDate(startAt);
  const startTime = formatDutchTime(startAt);
  const endDate = formatDutchDate(endAt);
  const endTime = formatDutchTime(endAt);
  if (startDate === endDate) {
    return `${startDate}, ${startTime} – ${endTime}`;
  }
  return `${startDate}, ${startTime} – ${endDate}, ${endTime}`;
}
