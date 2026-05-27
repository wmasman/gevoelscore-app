'use client';

import { useRouter } from 'next/navigation';
import { useState, type FormEvent } from 'react';

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
        setErrorMessage('Te veel pogingen. Probeer het straks opnieuw.');
        return;
      }
      if (!res.ok) {
        setStatus('error');
        setErrorMessage('Onjuiste e-mail of wachtwoord.');
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
      setErrorMessage('Er ging iets mis. Probeer het opnieuw.');
    } catch {
      setStatus('error');
      setErrorMessage('Verbindingsprobleem. Probeer het opnieuw.');
    }
  }

  const submitting = status === 'submitting';

  return (
    <form onSubmit={handleSubmit} className="space-y-4" noValidate={false}>
      <h1 className="text-2xl font-semibold text-center">Aanmelden</h1>

      <div>
        <label htmlFor="email" className="block text-sm font-medium mb-1">
          E-mailadres
        </label>
        <input
          id="email"
          name="email"
          type="email"
          autoComplete="email"
          autoFocus
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          disabled={submitting}
          className="w-full rounded border border-gray-300 px-3 py-3 text-base focus:border-blue-500 focus:outline-none disabled:opacity-60"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium mb-1">
          Wachtwoord
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
          className="w-full rounded border border-gray-300 px-3 py-3 text-base focus:border-blue-500 focus:outline-none disabled:opacity-60"
        />
      </div>

      {errorMessage !== null && (
        <p role="alert" className="text-sm text-red-600">
          {errorMessage}
        </p>
      )}

      <button
        type="submit"
        disabled={submitting}
        className="w-full rounded bg-blue-600 px-4 py-3 text-base font-semibold text-white hover:bg-blue-700 disabled:opacity-60"
      >
        {submitting ? 'Even geduld…' : 'Aanmelden'}
      </button>
    </form>
  );
}
