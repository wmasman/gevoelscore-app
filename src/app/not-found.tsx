import Link from 'next/link';
import { copy } from '@/copy';

export default function NotFound() {
  return (
    <main className="flex min-h-screen items-center justify-center p-8">
      <div className="max-w-sm text-center">
        <h1 className="text-2xl font-semibold">{copy.errors.notFound}</h1>
        <Link
          href="/"
          className="mt-6 inline-block rounded-md bg-[var(--color-accent)] px-4 py-2 text-white"
        >
          Naar startpagina
        </Link>
      </div>
    </main>
  );
}
