import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { TodayShell } from '@/components/today-shell';
import { readDayEntriesInRange, readDayEntryByDate } from '@/lib/api/day-entries';
import { readAllTags } from '@/lib/api/tags';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { SESSION_COOKIE_NAME } from '@/lib/auth/session';
import type { DayEntry } from '@/lib/domain/day-entry';
import { todayInAmsterdam } from '@/lib/domain/date';
import type { Tag } from '@/lib/domain/tag';

// Home / Today screen. Server component: presence-only auth check (full
// session validation happens on actual API calls from the wheel/note/tags
// in Step 4+). Matches the trade-off documented in
// docs/features/auth-hardening/step-1-bind-tfa-secret.md — stricter
// page-level checks break placeholder-cookie e2e fixtures, and the API
// routes already do strict validation when it matters.
//
// On a stale cookie: render the shell empty. The first save attempt will
// fail 401 and the standard error handler returns the user to /login.
//
// Step 6 added the 30-day timeline fetch in parallel with today's entry +
// allTags. Three reads, fired concurrently.

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

  const today = todayInAmsterdam();
  const session = await getValidatedSession(sessionId);
  let entry: DayEntry | null = null;
  let allTags: Tag[] = [];
  let timelineEntries: DayEntry[] = [];
  if (session !== null) {
    const from = shiftDate(today, -(TIMELINE_DAYS - 1));
    const [entryResult, tagsResult, rangeResult] = await Promise.all([
      readDayEntryByDate(session.accessToken, today),
      readAllTags(session.accessToken),
      readDayEntriesInRange(session.accessToken, from, today),
    ]);
    if (entryResult.ok) entry = entryResult.value;
    if (tagsResult.ok) allTags = tagsResult.value;
    if (rangeResult.ok) timelineEntries = rangeResult.value;
  }

  return (
    <TodayShell
      date={today}
      entry={entry}
      allTags={allTags}
      timelineEntries={timelineEntries}
    />
  );
}
