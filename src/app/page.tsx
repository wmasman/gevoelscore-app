import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { TodayShell } from '@/components/today-shell';
import { readDayEntryByDate } from '@/lib/api/day-entries';
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

export default async function HomePage() {
  const cookieStore = await cookies();
  const sessionId = cookieStore.get(SESSION_COOKIE_NAME)?.value ?? null;
  if (!sessionId) {
    redirect('/login');
  }

  const today = todayInAmsterdam();
  const session = await getValidatedSession(sessionId);
  // If the cookie is present but the session has expired or never existed
  // server-side, fall through with no entry — let the user see the shell.
  // Step 4's first save will surface the auth state via 401.
  let entry: DayEntry | null = null;
  let allTags: Tag[] = [];
  if (session !== null) {
    const [entryResult, tagsResult] = await Promise.all([
      readDayEntryByDate(session.accessToken, today),
      readAllTags(session.accessToken),
    ]);
    if (entryResult.ok) entry = entryResult.value;
    if (tagsResult.ok) allTags = tagsResult.value;
  }

  return <TodayShell date={today} entry={entry} allTags={allTags} />;
}
