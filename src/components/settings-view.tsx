'use client';

// SettingsView — the body of /settings. v1 surface is intentionally
// minimal: just the Account section (logout) plus a "binnenkort" pair
// for Export and Delete-account. Those land later (Track A3 / v1.5).
//
// Logout flow: two taps to avoid brainfog accidents. Tap the primary
// "Uitloggen" button, get an inline confirm ("Weet je het zeker?"),
// tap "Ja, uitloggen" to actually POST /api/auth/logout. On success the
// route handler clears the gs_session cookie + evicts the server-side
// session, and we router.push('/login').
//
// We use router.push (client-side nav) rather than location.assign so
// the SPA stays warm — the next /login render is server-side anyway.

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { copy } from '@/copy';

type LogoutState = 'idle' | 'confirming' | 'submitting' | 'error';

export function SettingsView() {
  const router = useRouter();
  const [state, setState] = useState<LogoutState>('idle');

  async function performLogout(): Promise<void> {
    setState('submitting');
    try {
      const res = await fetch('/api/auth/logout', {
        method: 'POST',
        credentials: 'same-origin',
      });
      if (!res.ok) {
        setState('error');
        return;
      }
      router.push('/login');
    } catch {
      setState('error');
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-120 flex-col gap-8 p-6">
      <header className="flex items-baseline justify-between gap-3">
        <h1 className="text-2xl font-semibold">{copy.settings.title}</h1>
        <Link
          href="/"
          className="text-sm text-fg-muted underline-offset-2 hover:underline focus-visible:outline-2 focus-visible:outline-accent"
        >
          {copy.settings.back}
        </Link>
      </header>

      <section className="flex flex-col gap-3">
        <h2 className="text-lg font-medium text-fg">{copy.settings.accountHeading}</h2>
        {state === 'confirming' || state === 'submitting' ? (
          <div className="flex flex-col gap-3 rounded-md border border-border bg-surface p-4">
            <p className="text-base text-fg">{copy.settings.logoutConfirmPrompt}</p>
            <div className="flex gap-3">
              <button
                type="button"
                onClick={() => void performLogout()}
                disabled={state === 'submitting'}
                className="rounded-md bg-accent-hover px-4 py-2 text-base font-medium text-bg disabled:opacity-60"
              >
                {copy.settings.logoutConfirmYes}
              </button>
              <button
                type="button"
                onClick={() => setState('idle')}
                disabled={state === 'submitting'}
                className="rounded-md border border-border px-4 py-2 text-base text-fg-muted disabled:opacity-60"
              >
                {copy.settings.logoutConfirmCancel}
              </button>
            </div>
          </div>
        ) : (
          <button
            type="button"
            onClick={() => setState('confirming')}
            className="self-start rounded-md border border-border px-4 py-2 text-base text-fg hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
          >
            {copy.settings.logout}
          </button>
        )}
        {state === 'error' && (
          <p role="alert" className="text-sm text-fg">
            {copy.settings.logoutError}
          </p>
        )}
      </section>

      <section className="flex flex-col gap-2">
        <h2 className="text-lg font-medium text-fg">{copy.settings.dataHeading}</h2>
        <ul className="flex flex-col gap-1 text-base text-fg-muted">
          <li className="flex items-baseline justify-between gap-3">
            <span>{copy.settings.dataExport}</span>
            <span className="text-xs uppercase tracking-wide text-fg-subtle">
              {copy.settings.dataSoon}
            </span>
          </li>
          <li className="flex items-baseline justify-between gap-3">
            <span>{copy.settings.dataDelete}</span>
            <span className="text-xs uppercase tracking-wide text-fg-subtle">
              {copy.settings.dataSoon}
            </span>
          </li>
        </ul>
      </section>
    </main>
  );
}
