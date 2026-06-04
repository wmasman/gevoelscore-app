import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { ChooseCalendarsForm } from '@/components/choose-calendars-form';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { SESSION_COOKIE_NAME } from '@/lib/auth/session';
import { isUuidShape } from '@/lib/domain/uuid';

// /settings/kalenders/choose?connection_id=<UUID> — landing page for
// the OAuth callback's 302. Auth-gated like /settings. The connection
// row was created in the callback; this screen lets the user pick
// which of their Google calendars to include for sync.

type SearchParams = Promise<{ connection_id?: string }>;

export default async function ChooseCalendarsPage({
  searchParams,
}: {
  searchParams: SearchParams;
}) {
  const cookieStore = await cookies();
  const sessionId = cookieStore.get(SESSION_COOKIE_NAME)?.value ?? null;
  if (!sessionId) {
    redirect('/login');
  }
  const session = await getValidatedSession(sessionId);
  if (session === null) {
    redirect('/login');
  }

  const { connection_id } = await searchParams;
  if (!connection_id || !isUuidShape(connection_id)) {
    redirect('/settings');
  }

  return <ChooseCalendarsForm connectionId={connection_id} />;
}
