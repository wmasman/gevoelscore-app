'use client';

// ChooseCalendarsForm — v1.6 Phase 1.E.2 + v1.6.1 exclude-delete UX.
//
// Renders the post-OAuth calendar-selection screen at
// /settings/kalenders/choose?connection_id=<UUID>. Also reachable from
// Settings → Kalenders → "Pas selectie aan" for an existing connection.
//
// On mount: GET /api/calendars/[id]/calendars to list the user's Google
// calendars plus the CURRENT included_calendar_ids and per-calendar
// event counts. Checkboxes default to the current selection (or all
// checked when there is no prior selection — first-time connect path).
//
// On submit: compute which calendars the user JUST removed. If any of
// those have existing events in the DB, show a confirm dialog asking
// whether to delete those events. The POST carries:
//   { included_calendar_ids, delete_excluded_calendar_events: bool }
// The server only deletes when the flag is true AND the removed list
// is non-empty.
//
// Loading + error states are rendered inline. Cancel returns to
// /settings without committing.

import { useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import { copy } from '@/copy';

type Calendar = { id: string; displayName: string; isPrimary: boolean };

type State =
  | { kind: 'loading' }
  | {
      kind: 'ready';
      calendars: Calendar[];
      initialIncluded: string[];
      eventCounts: Record<string, number>;
    }
  | {
      kind: 'confirmingDelete';
      calendars: Calendar[];
      initialIncluded: string[];
      eventCounts: Record<string, number>;
      removedCalendarIds: string[];
    }
  | {
      kind: 'submitting';
      calendars: Calendar[];
      initialIncluded: string[];
      eventCounts: Record<string, number>;
    }
  | { kind: 'loadError' }
  | {
      kind: 'submitError';
      calendars: Calendar[];
      initialIncluded: string[];
      eventCounts: Record<string, number>;
    };

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
        const body = (await res.json()) as {
          calendars?: Calendar[];
          included_calendar_ids?: string[];
          event_counts_by_calendar_id?: Record<string, number>;
        };
        const calendars = body.calendars ?? [];
        const initialIncluded = body.included_calendar_ids ?? [];
        const eventCounts = body.event_counts_by_calendar_id ?? {};
        setState({
          kind: 'ready',
          calendars,
          initialIncluded,
          eventCounts,
        });
        // Default: pre-check the user's current selection. If they have
        // none (first connect), default to ALL checked.
        if (initialIncluded.length > 0) {
          setSelected(new Set(initialIncluded));
        } else {
          setSelected(new Set(calendars.map((c) => c.id)));
        }
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

  // First-stage submit: figure out whether we need to ask about deletion
  // before sending. We only ask when:
  //   - At least one calendar was previously included and is now unchecked
  //   - AND at least one of those removed calendars has a non-zero event count
  // Otherwise we go straight to the POST (no delete).
  function submit(): void {
    if (state.kind !== 'ready' && state.kind !== 'submitError') return;
    const oldIds = new Set(state.initialIncluded);
    const removedCalendarIds = [...oldIds].filter((id) => !selected.has(id));
    const removedWithEvents = removedCalendarIds.filter(
      (id) => (state.eventCounts[id] ?? 0) > 0,
    );
    if (removedWithEvents.length === 0) {
      void post(false);
      return;
    }
    setState({
      kind: 'confirmingDelete',
      calendars: state.calendars,
      initialIncluded: state.initialIncluded,
      eventCounts: state.eventCounts,
      removedCalendarIds,
    });
  }

  async function post(deleteExcluded: boolean): Promise<void> {
    if (
      state.kind !== 'ready' &&
      state.kind !== 'submitError' &&
      state.kind !== 'confirmingDelete'
    ) {
      return;
    }
    const base = state;
    setState({
      kind: 'submitting',
      calendars: base.calendars,
      initialIncluded: base.initialIncluded,
      eventCounts: base.eventCounts,
    });
    try {
      const res = await fetch(`/api/calendars/${connectionId}/calendars`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          included_calendar_ids: [...selected],
          delete_excluded_calendar_events: deleteExcluded,
        }),
      });
      if (!res.ok) {
        setState({
          kind: 'submitError',
          calendars: base.calendars,
          initialIncluded: base.initialIncluded,
          eventCounts: base.eventCounts,
        });
        return;
      }
      router.push('/settings');
    } catch {
      setState({
        kind: 'submitError',
        calendars: base.calendars,
        initialIncluded: base.initialIncluded,
        eventCounts: base.eventCounts,
      });
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

      {(state.kind === 'ready' ||
        state.kind === 'submitting' ||
        state.kind === 'submitError' ||
        state.kind === 'confirmingDelete') && (
        <>
          <ul className="flex flex-col gap-2">
            {state.calendars.map((c) => {
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
                    disabled={
                      state.kind === 'submitting' ||
                      state.kind === 'confirmingDelete'
                    }
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
              onClick={submit}
              disabled={
                state.kind === 'submitting' ||
                state.kind === 'confirmingDelete'
              }
              className="inline-flex min-h-11 items-center rounded-md bg-accent px-4 py-2 text-base font-medium text-bg hover:bg-accent-hover focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
            >
              {state.kind === 'submitting' ? t.submitting : t.submit}
            </button>
            <button
              type="button"
              onClick={cancel}
              disabled={
                state.kind === 'submitting' ||
                state.kind === 'confirmingDelete'
              }
              className="inline-flex min-h-11 items-center rounded-md border border-border px-4 py-2 text-base text-fg-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
            >
              {t.cancel}
            </button>
          </div>

          {state.kind === 'confirmingDelete' && (
            <ExcludeConfirm
              calendars={state.calendars}
              removedCalendarIds={state.removedCalendarIds}
              eventCounts={state.eventCounts}
              onDelete={() => void post(true)}
              onKeep={() => void post(false)}
              onCancel={() =>
                setState({
                  kind: 'ready',
                  calendars: state.calendars,
                  initialIncluded: state.initialIncluded,
                  eventCounts: state.eventCounts,
                })
              }
            />
          )}
        </>
      )}
    </main>
  );
}

function ExcludeConfirm({
  calendars,
  removedCalendarIds,
  eventCounts,
  onDelete,
  onKeep,
  onCancel,
}: {
  calendars: Calendar[];
  removedCalendarIds: string[];
  eventCounts: Record<string, number>;
  onDelete: () => void;
  onKeep: () => void;
  onCancel: () => void;
}) {
  const t = copy.settings.calendars.choose.excludeConfirm;
  const namesById = useMemo(() => {
    const m = new Map<string, string>();
    for (const c of calendars) m.set(c.id, c.displayName);
    return m;
  }, [calendars]);

  const rows = removedCalendarIds
    .map((id) => ({ id, name: namesById.get(id) ?? id, n: eventCounts[id] ?? 0 }))
    .filter((r) => r.n > 0);
  const total = rows.reduce((sum, r) => sum + r.n, 0);

  return (
    <div
      role="alertdialog"
      aria-modal="true"
      aria-labelledby="exclude-confirm-title"
      className="fixed inset-0 z-50 flex items-end justify-center bg-bg/70 p-4 sm:items-center"
    >
      <div className="flex w-full max-w-120 flex-col gap-4 rounded-md border border-border bg-surface p-6">
        <h2
          id="exclude-confirm-title"
          className="text-lg font-semibold text-fg"
        >
          {t.title(total)}
        </h2>
        <p className="text-base text-fg-muted">{t.body}</p>
        <ul className="flex flex-col gap-1 text-sm text-fg">
          {rows.map((r) => (
            <li key={r.id}>
              {r.id === '(unknown)' ? t.rowUnknown(r.n) : t.row(r.name, r.n)}
            </li>
          ))}
        </ul>
        <div className="mt-2 flex flex-col gap-2 sm:flex-row sm:justify-end">
          <button
            type="button"
            onClick={onCancel}
            className="inline-flex min-h-11 items-center justify-center rounded-md border border-border px-4 py-2 text-base text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
          >
            {t.cancelButton}
          </button>
          <button
            type="button"
            onClick={onKeep}
            className="inline-flex min-h-11 items-center justify-center rounded-md border border-border px-4 py-2 text-base text-fg hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
          >
            {t.keepButton}
          </button>
          <button
            type="button"
            onClick={onDelete}
            className="inline-flex min-h-11 items-center justify-center rounded-md bg-accent px-4 py-2 text-base font-medium text-bg hover:bg-accent-hover focus-visible:outline-2 focus-visible:outline-accent"
          >
            {t.deleteButton}
          </button>
        </div>
      </div>
    </div>
  );
}
