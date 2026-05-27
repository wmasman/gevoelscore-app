'use client';

import { useRouter } from 'next/navigation';
import { useRef, useState, type ChangeEvent } from 'react';

type Status = 'idle' | 'submitting' | 'error';

export function VerifyForm() {
  const router = useRouter();
  const [otp, setOtp] = useState('');
  const [status, setStatus] = useState<Status>('idle');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const inFlightRef = useRef(false);

  async function submit(code: string) {
    if (inFlightRef.current) return;
    inFlightRef.current = true;
    setStatus('submitting');
    setErrorMessage(null);

    try {
      const res = await fetch('/api/auth/login/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ otp: code }),
      });

      if (res.status === 429) {
        setStatus('error');
        setErrorMessage('Te veel pogingen. Probeer het straks opnieuw.');
        setOtp('');
        return;
      }
      if (!res.ok) {
        setStatus('error');
        setErrorMessage('Code ongeldig.');
        setOtp('');
        return;
      }

      const body = (await res.json()) as { ok?: true };
      if (body.ok) {
        router.push('/');
        return;
      }

      setStatus('error');
      setErrorMessage('Er ging iets mis. Probeer het opnieuw.');
      setOtp('');
    } catch {
      setStatus('error');
      setErrorMessage('Verbindingsprobleem. Probeer het opnieuw.');
      setOtp('');
    } finally {
      inFlightRef.current = false;
    }
  }

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    // Filter non-digits and clamp to 6 chars.
    const digits = event.target.value.replace(/\D/g, '').slice(0, 6);
    setOtp(digits);
    if (digits.length === 6) {
      void submit(digits);
    }
  }

  const submitting = status === 'submitting';

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (otp.length === 6) void submit(otp);
      }}
      className="space-y-4"
    >
      <h1 className="text-2xl font-semibold text-center">Verificatiecode</h1>
      <p className="text-sm text-gray-600 text-center">
        Voer de 6-cijferige code uit je authenticator-app in.
      </p>

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
          onChange={handleChange}
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
