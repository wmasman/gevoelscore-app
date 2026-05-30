import Link from 'next/link';
import { copy } from '@/copy';

export default function NotFound() {
  return (
    <main className="flex min-h-dvh items-center justify-center p-8 pb-[max(2rem,env(safe-area-inset-bottom))]">
      <div className="max-w-sm text-center">
        <h1 className="text-2xl font-semibold">{copy.errors.notFound}</h1>
        <Link
          href="/"
          className="mt-6 inline-flex min-h-11 items-center rounded-md bg-accent px-4 py-2 text-bg focus-visible:outline-2 focus-visible:outline-accent"
        >
          Naar startpagina
        </Link>
      </div>
    </main>
  );
}
