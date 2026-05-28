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
        <p className="text-sm text-fg-muted text-center">
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
            // eslint-disable-next-line jsx-a11y/no-autofocus -- single-input phase of the 2FA setup wizard; brainfog sub-10s target. See frontend-conventions.md.
            autoFocus
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={submitting}
            className="w-full rounded-md border border-border bg-surface px-3 py-3 text-base text-fg focus:border-accent focus:outline-none focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
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
        <p className="text-sm text-fg-muted text-center">
          Voeg deze sleutel toe aan je authenticator-app (1Password, Google Authenticator, …) en
          voer vervolgens de 6-cijferige code in.
        </p>

        <div className="rounded-md border border-border bg-surface-muted p-3 text-sm break-all font-mono text-fg">
          <div className="mb-2">
            <span className="text-xs text-fg-subtle uppercase">Sleutel</span>
            <div data-testid="tfa-secret">{secret}</div>
          </div>
          <div>
            <span className="text-xs text-fg-subtle uppercase">otpauth URL</span>
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
            // eslint-disable-next-line jsx-a11y/no-autofocus -- single-input phase of the 2FA setup wizard; user came here to type 6 digits. See frontend-conventions.md.
            autoFocus
            value={otp}
            onChange={handleOtpChange}
            disabled={submitting}
            className="w-full rounded-md border border-border bg-surface px-3 py-3 text-2xl tracking-widest text-center font-mono text-fg focus:border-accent focus:outline-none focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
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

        {submitting && <p className="text-sm text-fg-muted text-center">Controleren…</p>}
      </form>
    );
  }

  // phase === 'done'
  return (
    <div className="space-y-4 text-center">
      <h1 className="text-2xl font-semibold">2FA actief</h1>
      <p className="text-sm text-fg-muted">Je wordt teruggebracht naar de app.</p>
    </div>
  );
}
