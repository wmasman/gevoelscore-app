import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { SettingsView } from '@/components/settings-view';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { SESSION_COOKIE_NAME } from '@/lib/auth/session';

// /settings — v1 surface: logout + binnenkort stubs for export + delete.
//
// Auth-gated with the same two-tier redirect as the home page (ADR 0005):
// missing cookie OR session-not-in-store → /login. We don't want a stale
// cookie to dump the user into a "log out" screen they can't act on.

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
  return <SettingsView />;
}
