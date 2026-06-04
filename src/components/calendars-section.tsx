'use client';

// CalendarsSection — v1.6 Settings → Kalenders surface.
//
// Empty state: a single "Verbind Google Calendar" button.
// Connected state: one row per calendar_connection with email +
// relative last-sync time + Ververs/Ontkoppel actions.
//
// Ontkoppel is irreversible (cascades calendar_events + series_exclusions
// + revokes the Google grant), so a two-tap confirm with focus-on-Annuleer
// gates it — same brainfog-protective pattern as logout in settings-view.
//
// "Verbind een andere kalender" surface is rendered (greyed) below the
// list as a forward marker for Outlook / Apple per the calendar-binding
// roadmap (v2 second-provider step).

import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { copy } from '@/copy';
import type { DirectusCalendarConnectionRow } from '@/lib/api/calendars';
import { relativeDutchTime } from '@/lib/domain/relative-dutch-time';

type Props = {
  connections: DirectusCalendarConnectionRow[];
  /**
   * Test-only override for `new Date()`. Production passes nothing →
   * the component reads the wall clock when rendering relative timestamps.
   */
  now?: Date;
};

type ActionState =
  | { kind: 'idle' }
  | { kind: 'connecting' }
  | { kind: 'syncing' }
  | { kind: 'confirmingDisconnect'; connectionId: string }
  | { kind: 'disconnecting'; connectionId: string };

export function CalendarsSection({ connections, now }: Props) {
  const t = copy.settings.calendars;
  const router = useRouter();
  const [state, setState] = useState<ActionState>({ kind: 'idle' });
  const [error, setError] = useState<string | null>(null);
  const cancelRef = useRef<HTMLButtonElement>(null);

  const currentNow = now ?? new Date();

  useEffect(() => {
    if (state.kind === 'confirmingDisconnect') {
      cancelRef.current?.focus();
    }
  }, [state.kind]);

  async function connect(): Promise<void> {
    setError(null);
    setState({ kind: 'connecting' });
    try {
      const res = await fetch('/api/calendars/google/connect', {
        method: 'POST',
        credentials: 'same-origin',
      });
      if (!res.ok) {
        setError(t.connectError);
        setState({ kind: 'idle' });
        return;
      }
      const body = (await res.json()) as { redirect_url?: string };
      if (!body.redirect_url) {
        setError(t.connectError);
        setState({ kind: 'idle' });
        return;
      }
      window.location.href = body.redirect_url;
    } catch {
      setError(t.connectError);
      setState({ kind: 'idle' });
    }
  }

  async function refresh(): Promise<void> {
    setError(null);
    setState({ kind: 'syncing' });
    try {
      const res = await fetch('/api/calendars/sync', {
        method: 'POST',
        credentials: 'same-origin',
      });
      if (!res.ok) {
        setError(t.refreshError);
        setState({ kind: 'idle' });
        return;
      }
      router.refresh();
      setState({ kind: 'idle' });
    } catch {
      setError(t.refreshError);
      setState({ kind: 'idle' });
    }
  }

  async function disconnect(connectionId: string): Promise<void> {
    setError(null);
    setState({ kind: 'disconnecting', connectionId });
    try {
      const res = await fetch(`/api/calendars/${connectionId}/disconnect`, {
        method: 'POST',
        credentials: 'same-origin',
      });
      if (!res.ok) {
        setError(t.disconnectError);
        setState({ kind: 'idle' });
        return;
      }
      const body = (await res.json()) as { revoke_ok?: boolean };
      router.refresh();
      setState({ kind: 'idle' });
      if (body.revoke_ok === false) {
        setError(t.revokeFailedWarning);
      }
    } catch {
      setError(t.disconnectError);
      setState({ kind: 'idle' });
    }
  }

  const isBusy = state.kind !== 'idle' && state.kind !== 'confirmingDisconnect';

  return (
    <section className="flex flex-col gap-3" aria-labelledby="calendars-heading">
      <h2 id="calendars-heading" className="text-lg font-medium text-fg">
        {t.heading}
      </h2>

      {connections.length === 0 ? (
        <div className="flex flex-col items-start gap-3">
          <p className="text-base text-fg-muted">{t.emptyState}</p>
          <button
            type="button"
            onClick={() => void connect()}
            disabled={isBusy}
            className="inline-flex min-h-11 items-center rounded-md bg-accent px-4 py-2 text-base font-medium text-bg hover:bg-accent-hover focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
          >
            {state.kind === 'connecting' ? t.refreshing : t.connectGoogle}
          </button>
        </div>
      ) : (
        <ul className="flex flex-col gap-3">
          {connections.map((conn) => {
            const lastSyncDate = conn.last_synced_at ? new Date(conn.last_synced_at) : null;
            const relative = lastSyncDate
              ? t.lastSyncedAt(relativeDutchTime(lastSyncDate, currentNow))
              : t.neverSynced;
            const statusLabel =
              conn.status === 'active'
                ? t.statusActive
                : conn.status === 'error'
                  ? t.statusError
                  : t.statusDisconnected;
            const isConfirming =
              state.kind === 'confirmingDisconnect' && state.connectionId === conn.id;
            const isDisconnecting =
              state.kind === 'disconnecting' && state.connectionId === conn.id;

            return (
              <li
                key={conn.id}
                className="flex flex-col gap-2 rounded-md border border-border bg-surface p-4"
              >
                <div className="flex flex-col gap-1">
                  <p className="text-base font-medium text-fg">{t.rowLabel(conn.provider_account_email)}</p>
                  <p className="text-sm text-fg-muted">
                    {statusLabel} · {relative}
                  </p>
                  {conn.last_sync_error && (
                    <p className="text-sm text-fg" role="alert">
                      {conn.last_sync_error}
                    </p>
                  )}
                </div>

                {isConfirming || isDisconnecting ? (
                  <div
                    role="alertdialog"
                    aria-labelledby={`disconnect-confirm-prompt-${conn.id}`}
                    className="flex flex-col gap-3 rounded-md border border-border bg-bg p-3"
                  >
                    <p
                      id={`disconnect-confirm-prompt-${conn.id}`}
                      className="text-sm text-fg"
                    >
                      {t.disconnectConfirmPrompt}
                    </p>
                    <div className="flex gap-3">
                      <button
                        type="button"
                        onClick={() => void disconnect(conn.id)}
                        disabled={isDisconnecting}
                        className="inline-flex min-h-11 items-center rounded-md bg-accent-hover px-4 py-2 text-base font-medium text-bg focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
                      >
                        {isDisconnecting ? t.disconnecting : t.disconnectConfirmYes}
                      </button>
                      <button
                        ref={cancelRef}
                        type="button"
                        onClick={() => setState({ kind: 'idle' })}
                        disabled={isDisconnecting}
                        className="inline-flex min-h-11 items-center rounded-md border border-border px-4 py-2 text-base text-fg-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
                      >
                        {t.disconnectConfirmCancel}
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="flex gap-2">
                    <button
                      type="button"
                      onClick={() => void refresh()}
                      disabled={isBusy}
                      className="inline-flex min-h-11 items-center rounded-md border border-border px-4 py-2 text-base text-fg hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
                    >
                      {state.kind === 'syncing' ? t.refreshing : t.refresh}
                    </button>
                    <button
                      type="button"
                      onClick={() =>
                        setState({ kind: 'confirmingDisconnect', connectionId: conn.id })
                      }
                      disabled={isBusy}
                      className="inline-flex min-h-11 items-center rounded-md border border-border px-4 py-2 text-base text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
                    >
                      {t.disconnect}
                    </button>
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      )}

      {error && (
        <p role="alert" className="text-sm text-fg">
          {error}
        </p>
      )}

      {connections.length > 0 && (
        <p className="text-xs text-fg-subtle">{t.otherComingSoon}</p>
      )}
    </section>
  );
}
