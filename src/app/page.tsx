import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { TodayShell } from '@/components/today-shell';
import { readDayEntriesInRange, readDayEntryByDate } from '@/lib/api/day-entries';
import { readAllEpisodes } from '@/lib/api/episodes';
import { readAllTags } from '@/lib/api/tags';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { SESSION_COOKIE_NAME } from '@/lib/auth/session';
import type { DayEntry } from '@/lib/domain/day-entry';
import { todayInAmsterdam } from '@/lib/domain/date';
import type { Episode } from '@/lib/domain/episode';
import type { Tag } from '@/lib/domain/tag';

// Home / Today screen. Server component. Two redirects guard the render:
//   1. no session cookie → /login
//   2. cookie present but `getValidatedSession` returns null → /login
//      (most often: Fly machine restart wiped the in-memory store, so the
//      browser holds an id the server no longer knows about)
//
// The earlier "render empty on stale cookie" behaviour silently hid a
// destroyed-session state — the user saw a fresh-install-looking screen
// with no nudge to re-authenticate. See investigation 2026-05-28.
//
// Three reads (today's entry, all tags, 30-day timeline) fire concurrently
// once we have a validated session.

const TIMELINE_DAYS = 30;

function shiftDate(date: string, days: number): string {
  const parsed = new Date(`${date}T12:00:00Z`);
  parsed.setUTCDate(parsed.getUTCDate() + days);
  const y = parsed.getUTCFullYear();
  const m = String(parsed.getUTCMonth() + 1).padStart(2, '0');
  const d = String(parsed.getUTCDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

export default async function HomePage() {
  const cookieStore = await cookies();
  const sessionId = cookieStore.get(SESSION_COOKIE_NAME)?.value ?? null;
  if (!sessionId) {
    redirect('/login');
  }

  const session = await getValidatedSession(sessionId);
  if (session === null) {
    // Cookie present but the server-side store has no matching record (or
    // a refresh attempt failed). Common after a Fly machine restart, which
    // wipes the in-memory store. The user has to re-authenticate — the
    // alternative (rendering the shell with empty data) silently hides the
    // problem and looks identical to a brand-new user's first paint.
    redirect('/login');
  }

  const today = todayInAmsterdam();
  let entry: DayEntry | null = null;
  let allTags: Tag[] = [];
  let timelineEntries: DayEntry[] = [];
  let episodes: Episode[] = [];
  const from = shiftDate(today, -(TIMELINE_DAYS - 1));
  const [entryResult, tagsResult, rangeResult, episodesResult] = await Promise.all([
    readDayEntryByDate(session.accessToken, today),
    readAllTags(session.accessToken),
    readDayEntriesInRange(session.accessToken, from, today),
    // Active episodes only (v1.5 Periodes tab). Read failure falls
    // back to empty list — the other tabs continue to work, the
    // Periodes tab shows its empty state. Same fail-soft posture as
    // the other reads above.
    readAllEpisodes(session.accessToken),
  ]);
  if (entryResult.ok) entry = entryResult.value;
  if (tagsResult.ok) allTags = tagsResult.value;
  if (rangeResult.ok) timelineEntries = rangeResult.value;
  if (episodesResult.ok) episodes = episodesResult.value;

  return (
    <TodayShell
      date={today}
      entry={entry}
      allTags={allTags}
      timelineEntries={timelineEntries}
      episodes={episodes}
    />
  );
}
