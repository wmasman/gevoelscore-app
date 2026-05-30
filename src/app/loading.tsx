// Skeleton matching the post-load Today layout so there's no CLS when
// the real content swaps in. STATIC blocks — the prior `animate-pulse`
// shimmer was named in docs/design/brief.md as a forbidden decoration
// ("does this motion tell the user something they need to know?" —
// shimmer fails that test). Blank-but-correctly-shaped placeholders
// preserve layout without the decorative motion.

export default function Loading() {
  return (
    <main className="mx-auto flex min-h-dvh max-w-120 flex-col gap-6 p-6 pb-[max(1.5rem,env(safe-area-inset-bottom))]">
      <div className="h-8 w-48 rounded-md bg-surface-muted" />
      <div className="h-64 w-full rounded-lg bg-surface-muted" />
      <div className="h-12 w-full rounded-md bg-surface-muted" />
      <div className="flex flex-col gap-2">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="h-10 w-full rounded-md bg-surface-muted" />
        ))}
      </div>
    </main>
  );
}
