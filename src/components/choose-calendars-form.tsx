'use client';

// ChooseCalendarsForm — v1.6 Phase 1.E.2.
//
// Renders the post-OAuth calendar-selection screen at
// /settings/kalenders/choose?connection_id=<UUID>.
//
// On mount: GET /api/calendars/[id]/calendars to list the user's Google
// calendars. All checkboxes checked by default (per AC1.58). Submit
// POSTs the selected ids; on success, redirects back to /settings.
//
// Loading + error states are rendered inline. Cancel returns to
// /settings without committing — the connection row already exists
// (created by the callback), so cancelling leaves it with empty
// included_calendar_ids; the user can retry from Settings.

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { copy } from '@/copy';

type Calendar = { id: string; displayName: string; isPrimary: boolean };

type State =
  | { kind: 'loading' }
  | { kind: 'ready'; calendars: Calendar[] }
  | { kind: 'submitting' }
  | { kind: 'loadError' }
  | { kind: 'submitError' };

export function ChooseCalendarsForm({ connectionId }: { connectionId: string }) {
  const t = copy.settings.calendars.choose;
  const router = useRouter();
  const [state, setState] = useState<State>({ kind: 'loading' });
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setState({ kind: 'loading' });
    void (async () => {
      try {
        const res = await fetch(`/api/calendars/${connectionId}/calendars`, {
          credentials: 'same-origin',
        });
        if (cancelled) return;
        if (!res.ok) {
          setState({ kind: 'loadError' });
          return;
        }
        const body = (await res.json()) as { calendars?: Calendar[] };
        const calendars = body.calendars ?? [];
        setState({ kind: 'ready', calendars });
        // Default to ALL checked, per AC1.58.
        setSelected(new Set(calendars.map((c) => c.id)));
      } catch {
        if (!cancelled) setState({ kind: 'loadError' });
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [connectionId, reloadKey]);

  function toggle(id: string): void {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  async function submit(): Promise<void> {
    if (state.kind !== 'ready') return;
    setState({ kind: 'submitting' });
    try {
      const res = await fetch(`/api/calendars/${connectionId}/calendars`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ included_calendar_ids: [...selected] }),
      });
      if (!res.ok) {
        setState({ kind: 'submitError', calendars: state.calendars } as State);
        return;
      }
      router.push('/settings');
    } catch {
      setState({ kind: 'submitError', calendars: state.calendars } as State);
    }
  }

  function cancel(): void {
    router.push('/settings');
  }

  return (
    <main className="mx-auto flex min-h-dvh max-w-120 flex-col gap-6 p-6 pb-[max(1.5rem,env(safe-area-inset-bottom))]">
      <header className="flex flex-col gap-2">
        <h1 className="text-2xl font-semibold">{t.title}</h1>
        <p className="text-base text-fg-muted">{t.intro}</p>
      </header>

      {state.kind === 'loading' && (
        <p className="text-base text-fg-muted" role="status">
          {t.loading}
        </p>
      )}

      {state.kind === 'loadError' && (
        <div className="flex flex-col gap-3">
          <p className="text-base text-fg" role="alert">
            {t.loadError}
          </p>
          <button
            type="button"
            onClick={() => setReloadKey((k) => k + 1)}
            className="inline-flex min-h-11 items-center self-start rounded-md border border-border px-4 py-2 text-base text-fg hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
          >
            {t.retryLoad}
          </button>
        </div>
      )}

      {(state.kind === 'ready' || state.kind === 'submitting' || state.kind === 'submitError') && (
        <>
          <ul className="flex flex-col gap-2">
            {('calendars' in state ? state.calendars : []).map((c) => {
              const isChecked = selected.has(c.id);
              return (
                <li
                  key={c.id}
                  className="flex items-center gap-3 rounded-md border border-border bg-surface p-3"
                >
                  <input
                    type="checkbox"
                    id={`cal-${c.id}`}
                    checked={isChecked}
                    onChange={() => toggle(c.id)}
                    disabled={state.kind === 'submitting'}
                    className="h-5 w-5 accent-accent"
                  />
                  <label
                    htmlFor={`cal-${c.id}`}
                    className="flex flex-1 items-center justify-between gap-2 text-base text-fg"
                  >
                    <span>{c.displayName}</span>
                    {c.isPrimary && (
                      <span className="text-xs uppercase tracking-wide text-fg-subtle">
                        {t.primaryBadge}
                      </span>
                    )}
                  </label>
                </li>
              );
            })}
          </ul>

          {state.kind === 'submitError' && (
            <p role="alert" className="text-sm text-fg">
              {t.submitError}
            </p>
          )}

          <div className="flex gap-3">
            <button
              type="button"
              onClick={() => void submit()}
              disabled={state.kind === 'submitting'}
              className="inline-flex min-h-11 items-center rounded-md bg-accent px-4 py-2 text-base font-medium text-bg hover:bg-accent-hover focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
            >
              {state.kind === 'submitting' ? t.submitting : t.submit}
            </button>
            <button
              type="button"
              onClick={cancel}
              disabled={state.kind === 'submitting'}
              className="inline-flex min-h-11 items-center rounded-md border border-border px-4 py-2 text-base text-fg-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
            >
              {t.cancel}
            </button>
          </div>
        </>
      )}
    </main>
  );
}
