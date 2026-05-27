import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { SESSION_COOKIE_NAME } from '@/lib/auth/session';
import { SetupForm } from './setup-form';

// Server component: ensures the user is authenticated before showing the
// setup form. Middleware doesn't gate /login/* paths, so this page does
// its own presence check. Server-side cookie reads work for httpOnly.

export default async function TwoFactorSetupPage() {
  const cookieStore = await cookies();
  const session = cookieStore.get(SESSION_COOKIE_NAME);
  if (!session?.value) {
    redirect('/login');
  }
  return <SetupForm />;
}
