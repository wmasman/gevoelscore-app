import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { PENDING_OTP_COOKIE_NAME } from '@/lib/auth/pending-otp';
import { VerifyForm } from './verify-form';

// Server Component: enforces AC10 by reading the gs_pending_otp cookie on the
// server and redirecting to /login if it's missing. The cookie is httpOnly so
// client code can't check this — server-side is the only place that works.
//
// If the cookie is present but the server-side pending state has already
// expired, the user will get a 401 on form submit (handled in VerifyForm).

export default async function VerifyPage() {
  const cookieStore = await cookies();
  const pending = cookieStore.get(PENDING_OTP_COOKIE_NAME);
  if (!pending || !pending.value) {
    redirect('/login');
  }
  return <VerifyForm />;
}
