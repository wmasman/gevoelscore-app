import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { SettingsView } from '@/components/settings-view';
import { readActiveConnectionsForUser } from '@/lib/api/calendars';
import type { DirectusCalendarConnectionRow } from '@/lib/api/calendars';
import { readDayEntriesInRange } from '@/lib/api/day-entries';
import { readAllEpisodes } from '@/lib/api/episodes';
import { readAllTags } from '@/lib/api/tags';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { SESSION_COOKIE_NAME } from '@/lib/auth/session';
import type { DayEntry } from '@/lib/domain/day-entry';
import { todayInAmsterdam } from '@/lib/domain/date';
import type { Episode } from '@/lib/domain/episode';
import type { Tag } from '@/lib/domain/tag';

// /settings — v1 surface: logout + binnenkort stubs for export + delete.
// v1.5b: + Tag-beheer section (between Account and Data) for tag
// management — rename / recategorize / archive / un-archive / re-parent /
// hard-delete (gated by usage_count === 0).
//
// Auth-gated with the same two-tier redirect as the home page (ADR 0005):
// missing cookie OR session-not-in-store → /login. We don't want a stale
// cookie to dump the user into a "log out" screen they can't act on.
//
// After auth, the three reads (allTags + episodes + 90-day day_entries
// for the recency-sort derivation) fire in parallel. Read failures fall
// back to empty arrays — the Tag-beheer section degrades to the empty-
// corpus state without blocking the rest of /settings.

const TIMELINE_DAYS = 90;

function shiftDate(date: string, days: number): string {
  const parsed = new Date(`${date}T12:00:00Z`);
  parsed.setUTCDate(parsed.getUTCDate() + days);
  const y = parsed.getUTCFullYear();
  const m = String(parsed.getUTCMonth() + 1).padStart(2, '0');
  const d = String(parsed.getUTCDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

export default async function SettingsPage() {
  const cookieStore = await cookies();
  const sessionId = cookieStore.get(SESSION_COOKIE_NAME)?.value ?? null;
  if (!sessionId) {
    redirect('/login');
  }
  const session = await getValidatedSession(sessionId);
  if (session === null) {
    redirect('/login');
  }

  const today = todayInAmsterdam();
  const from = shiftDate(today, -(TIMELINE_DAYS - 1));

  let allTags: Tag[] = [];
  let episodes: Episode[] = [];
  let timelineEntries: DayEntry[] = [];
  let calendarConnections: DirectusCalendarConnectionRow[] = [];
  // Settings → Tag-beheer must see archived tags too (the "Toon
  // gearchiveerd" toggle gates UI visibility, not the source list).
  // Episodes follows the same pattern via includeArchived: true.
  // v1.6 — calendar_connections for the Kalenders section. v1.6
  // single-user means the WILLEM_USER_ID env-var-resolved id is used;
  // multi-user (v2) will read user_id from the session.
  const willemUserId = process.env.WILLEM_USER_ID ?? '';
  const [tagsResult, episodesResult, rangeResult, connectionsResult] =
    await Promise.all([
      readAllTags(session.accessToken, { includeArchived: true }),
      readAllEpisodes(session.accessToken, { includeArchived: true }),
      readDayEntriesInRange(session.accessToken, from, today),
      willemUserId
        ? readActiveConnectionsForUser(session.accessToken, willemUserId)
        : Promise.resolve({ ok: true as const, value: [] }),
    ]);
  if (tagsResult.ok) allTags = tagsResult.value;
  if (episodesResult.ok) episodes = episodesResult.value;
  if (rangeResult.ok) timelineEntries = rangeResult.value;
  if (connectionsResult.ok) calendarConnections = connectionsResult.value;

  // v1.6.1 hydration fix: snapshot `now` here on the server and thread
  // it down. CalendarsSection's relative-time rendering ("2 uur geleden")
  // would otherwise compute `new Date()` once during SSR and once during
  // client hydration, drifting across thresholds in relativeDutchTime
  // and causing React #418 hydration mismatches (seen as 200+ console
  // errors on /settings). After router.refresh() this re-snapshots so
  // the displayed time stays roughly current.
  const now = new Date();

  return (
    <SettingsView
      allTags={allTags}
      episodes={episodes}
      timelineEntries={timelineEntries}
      calendarConnections={calendarConnections}
      now={now}
    />
  );
}
