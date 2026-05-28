// Skeleton matching the post-load Today layout so there's no CLS when the
// real content swaps in. Step 2 will pin the score wheel + tag-header
// dimensions; for now this is a minimal "we are loading" shell that fills
// the same vertical space.

export default function Loading() {
  return (
    <main className="mx-auto flex min-h-screen max-w-[480px] flex-col gap-6 p-6">
      <div className="h-8 w-48 animate-pulse rounded-md bg-[var(--color-border)]" />
      <div className="h-64 w-full animate-pulse rounded-lg bg-[var(--color-border)]" />
      <div className="h-12 w-full animate-pulse rounded-md bg-[var(--color-border)]" />
      <div className="flex flex-col gap-2">
        {Array.from({ length: 8 }).map((_, i) => (
          <div
            key={i}
            className="h-10 w-full animate-pulse rounded-md bg-[var(--color-border)]"
          />
        ))}
      </div>
    </main>
  );
}
