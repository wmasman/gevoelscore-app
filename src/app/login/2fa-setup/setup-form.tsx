'use client';

import { useRouter } from 'next/navigation';
import { useState, type ChangeEvent, type FormEvent } from 'react';

type Phase = 'password' | 'verify' | 'done';

export function SetupForm() {
  const router = useRouter();
  const [phase, setPhase] = useState<Phase>('password');
  const [password, setPassword] = useState('');
  const [secret, setSecret] = useState('');
  const [otpauthUrl, setOtpauthUrl] = useState('');
  const [otp, setOtp] = useState('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handlePasswordSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setErrorMessage(null);

    try {
      const res = await fetch('/api/auth/2fa/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password }),
      });

      if (res.status === 401) {
        const body = (await res.json().catch(() => ({}))) as { error?: string };
        if (body.error === 'invalid_password') {
          setErrorMessage('Wachtwoord onjuist.');
        } else {
          setErrorMessage('Sessie verlopen. Log opnieuw in.');
        }
        return;
      }
      if (!res.ok) {
        setErrorMessage('Er ging iets mis. Probeer het opnieuw.');
        return;
      }

      const body = (await res.json()) as { secret: string; otpauth_url: string };
      setSecret(body.secret);
      setOtpauthUrl(body.otpauth_url);
      setPassword('');
      setPhase('verify');
    } catch {
      setErrorMessage('Verbindingsprobleem. Probeer het opnieuw.');
    } finally {
      setSubmitting(false);
    }
  }

  async function handleOtpSubmit(code: string) {
    setSubmitting(true);
    setErrorMessage(null);

    try {
      const res = await fetch('/api/auth/2fa/enable', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ secret, otp: code }),
      });

      if (!res.ok) {
        setErrorMessage('Code ongeldig.');
        setOtp('');
        return;
      }

      setPhase('done');
      setTimeout(() => router.push('/'), 1500);
    } catch {
      setErrorMessage('Verbindingsprobleem. Probeer het opnieuw.');
      setOtp('');
    } finally {
      setSubmitting(false);
    }
  }

  function handleOtpChange(event: ChangeEvent<HTMLInputElement>) {
    const digits = event.target.value.replace(/\D/g, '').slice(0, 6);
    setOtp(digits);
    if (digits.length === 6) {
      void handleOtpSubmit(digits);
    }
  }

  if (phase === 'password') {
    return (
      <form onSubmit={handlePasswordSubmit} className="space-y-4">
        <h1 className="text-2xl font-semibold text-center">2FA instellen</h1>
        <p className="text-sm text-gray-600 text-center">
          Bevestig je wachtwoord om een TOTP-code te genereren.
        </p>

        <div>
          <label htmlFor="password" className="block text-sm font-medium mb-1">
            Wachtwoord
          </label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            autoFocus
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
          {submitting ? 'Even geduld…' : 'Genereer TOTP'}
        </button>
      </form>
    );
  }

  if (phase === 'verify') {
    return (
      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (otp.length === 6) void handleOtpSubmit(otp);
        }}
        className="space-y-4"
      >
        <h1 className="text-2xl font-semibold text-center">2FA bevestigen</h1>
        <p className="text-sm text-gray-600 text-center">
          Voeg deze sleutel toe aan je authenticator-app (1Password, Google Authenticator, …) en
          voer vervolgens de 6-cijferige code in.
        </p>

        <div className="rounded border border-gray-300 bg-gray-50 p-3 text-sm break-all font-mono">
          <div className="mb-2">
            <span className="text-xs text-gray-500 uppercase">Sleutel</span>
            <div data-testid="tfa-secret">{secret}</div>
          </div>
          <div>
            <span className="text-xs text-gray-500 uppercase">otpauth URL</span>
            <div data-testid="tfa-otpauth-url">{otpauthUrl}</div>
          </div>
        </div>

        <div>
          <label htmlFor="otp" className="block text-sm font-medium mb-1">
            Code
          </label>
          <input
            id="otp"
            name="otp"
            type="text"
            inputMode="numeric"
            pattern="[0-9]*"
            maxLength={6}
            autoComplete="one-time-code"
            autoFocus
            value={otp}
            onChange={handleOtpChange}
            disabled={submitting}
            className="w-full rounded border border-gray-300 px-3 py-3 text-2xl tracking-widest text-center font-mono focus:border-blue-500 focus:outline-none disabled:opacity-60"
          />
        </div>

        {errorMessage !== null && (
          <p role="alert" className="text-sm text-red-600">
            {errorMessage}
          </p>
        )}

        {submitting && <p className="text-sm text-gray-500 text-center">Controleren…</p>}
      </form>
    );
  }

  // phase === 'done'
  return (
    <div className="space-y-4 text-center">
      <h1 className="text-2xl font-semibold">2FA actief</h1>
      <p className="text-sm text-gray-600">Je wordt teruggebracht naar de app.</p>
    </div>
  );
}
