import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { SESSION_COOKIE_NAME } from '@/lib/auth/session';
import { SetupForm } from './setup-form';

// Server component: gates this page on cookie presence. Server-side cookie
// reads work for httpOnly. We deliberately stop at presence; the actual
// session-value validation happens on form submit via /api/auth/2fa/generate
// which uses getValidatedSession (with transparent refresh-token rotation).
//
// Trade-off: a user with a stale cookie sees the password form, enters
// their password, and only then gets "Sessie verlopen. Log opnieuw in"
// from the route. Acceptable — wasted one password entry vs. immediate
// redirect — and avoids needing a test-only session backdoor in the
// Playwright e2e suite.

export default async function TwoFactorSetupPage() {
  const cookieStore = await cookies();
  const session = cookieStore.get(SESSION_COOKIE_NAME);
  if (!session?.value) {
    redirect('/login');
  }
  return <SetupForm />;
}
