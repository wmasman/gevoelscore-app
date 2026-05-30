'use client';

import { useRouter } from 'next/navigation';
import { useState, type FormEvent } from 'react';
import { copy } from '@/copy';

type Status = 'idle' | 'submitting' | 'error';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState<Status>('idle');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatus('submitting');
    setErrorMessage(null);

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (res.status === 429) {
        setStatus('error');
        setErrorMessage(copy.auth.login.errors.rateLimited);
        return;
      }
      if (!res.ok) {
        setStatus('error');
        setErrorMessage(copy.auth.login.errors.invalidCredentials);
        return;
      }

      const body = (await res.json()) as { ok?: true; requires_otp?: true };
      if (body.requires_otp) {
        router.push('/login/verify');
        return;
      }
      if (body.ok) {
        router.push('/');
        return;
      }

      // Unexpected shape — treat as a generic error
      setStatus('error');
      setErrorMessage(copy.auth.login.errors.unknown);
    } catch {
      setStatus('error');
      setErrorMessage(copy.auth.login.errors.network);
    }
  }

  const submitting = status === 'submitting';

  return (
    <form onSubmit={handleSubmit} className="space-y-4" noValidate={false}>
      <h1 className="text-2xl font-semibold text-center">{copy.auth.login.title}</h1>

      <div>
        <label htmlFor="email" className="block text-sm font-medium mb-1">
          {copy.auth.login.emailLabel}
        </label>
        <input
          id="email"
          name="email"
          type="email"
          autoComplete="email"
          // eslint-disable-next-line jsx-a11y/no-autofocus -- single-input login page; brainfog sub-10s target. Discussed in frontend-conventions.md.
          autoFocus
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          disabled={submitting}
          className="w-full rounded-md border border-border bg-surface px-3 py-3 text-base text-fg placeholder:text-fg-muted focus:border-accent focus:outline-none focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium mb-1">
          {copy.auth.login.passwordLabel}
        </label>
        <input
          id="password"
          name="password"
          type="password"
          autoComplete="current-password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={submitting}
          className="w-full rounded-md border border-border bg-surface px-3 py-3 text-base text-fg placeholder:text-fg-muted focus:border-accent focus:outline-none focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
        />
      </div>

      {errorMessage !== null && (
        <div
          role="alert"
          className="rounded-md border border-border-strong bg-surface-muted px-3 py-2 text-sm text-fg"
        >
          {errorMessage}
        </div>
      )}

      <button
        type="submit"
        disabled={submitting}
        className="w-full rounded-md bg-accent-hover px-4 py-3 text-base font-semibold text-bg hover:bg-accent-active focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
      >
        {submitting ? copy.auth.login.submitting : copy.auth.login.submit}
      </button>
    </form>
  );
}
