'use client';

import { copy } from '@/copy';

// App-router error boundary. Renders for any uncaught error during render
// or in a server-component fetch. Deliberately generic — never leaks the
// error message or stack to the user (server errors may carry PII or
// Directus envelope detail). The technical detail goes to server logs.

export default function ErrorBoundary({
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <main className="flex min-h-dvh items-center justify-center p-8 pb-[max(2rem,env(safe-area-inset-bottom))]">
      <div className="max-w-sm text-center">
        <h1 className="text-2xl font-semibold">{copy.errors.generic}</h1>
        <button
          type="button"
          onClick={reset}
          className="mt-6 min-h-11 rounded-md bg-accent px-4 py-2 text-bg focus-visible:outline-2 focus-visible:outline-accent"
        >
          Probeer opnieuw
        </button>
      </div>
    </main>
  );
}
