'use client';

// CalendarEventSheet — v1.6 Phase 1.E.3.
//
// Per-event detail BottomSheet. One sheet with three internal views:
//   - 'main': title + datetime + location + linked-tag/episode chips +
//     [Koppel aan tag] + [Koppel aan periode] + [Sluit uit als context]
//     (or [Weer meenemen] when already excluded; recurring also shows
//     [Voeg hele serie weer toe] / [Sluit hele serie uit]).
//   - 'pickingTag': "← Terug" + tag list (with "Geen" to unlink).
//   - 'pickingEpisode': "← Terug" + episode list (with "Geen" to unlink).
//
// All mutations go to the existing routes:
//   - PATCH /api/calendars/events/[id] for linked_tag_id / linked_episode_id
//     and included_as_context (route handles series-exclusion side effect).
//   - POST /api/calendars/events/[id]/include-series for the symmetric
//     re-include of a whole recurring series.
//
// On any successful mutation: router.refresh() + close the sheet (the
// parent renders the next state). On failure: inline error, sheet stays
// open.

import { useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { BottomSheet } from '@/components/lab/bottom-sheet';
import { copy } from '@/copy';
import type { DirectusCalendarEventRow } from '@/lib/api/calendars';
import type { Episode } from '@/lib/domain/episode';
import { formatEventDateTime } from '@/lib/domain/event-display';
import type { Tag } from '@/lib/domain/tag';

type Props = {
  event: DirectusCalendarEventRow;
  tags: Tag[];
  episodes: Episode[];
  open: boolean;
  onClose: () => void;
};

type View = 'main' | 'pickingTag' | 'pickingEpisode';
type ActionState = 'idle' | 'submitting' | 'error';

export function CalendarEventSheet({
  event,
  tags,
  episodes,
  open,
  onClose,
}: Props) {
  const t = copy.settings.calendars.eventSheet;
  const router = useRouter();
  const [view, setView] = useState<View>('main');
  const [action, setAction] = useState<ActionState>('idle');
  const closeRef = useRef<HTMLButtonElement>(null);

  // Resolve display values
  const startAt = new Date(event.start_at);
  const endAt = new Date(event.end_at);
  const dateTimeLabel = formatEventDateTime(startAt, endAt, event.all_day);
  const linkedTag = tags.find((tg) => tg.id === event.linked_tag_id) ?? null;
  const linkedEpisode = episodes.find((ep) => ep.id === event.linked_episode_id) ?? null;
  const isRecurring = event.recurrence_id !== null;
  const isExcluded = event.included_as_context === false;

  async function patch(body: Record<string, unknown>): Promise<boolean> {
    setAction('submitting');
    try {
      const res = await fetch(`/api/calendars/events/${event.id}`, {
        method: 'PATCH',
        credentials: 'same-origin',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(body),
      });
      if (!res.ok) {
        setAction('error');
        return false;
      }
      router.refresh();
      setAction('idle');
      return true;
    } catch {
      setAction('error');
      return false;
    }
  }

  async function postIncludeSeries(): Promise<boolean> {
    setAction('submitting');
    try {
      const res = await fetch(
        `/api/calendars/events/${event.id}/include-series`,
        {
          method: 'POST',
          credentials: 'same-origin',
        },
      );
      if (!res.ok) {
        setAction('error');
        return false;
      }
      router.refresh();
      setAction('idle');
      return true;
    } catch {
      setAction('error');
      return false;
    }
  }

  async function handlePickTag(tagId: string | null): Promise<void> {
    const ok = await patch({ linked_tag_id: tagId });
    if (ok) {
      setView('main');
      onClose();
    }
  }

  async function handlePickEpisode(episodeId: string | null): Promise<void> {
    const ok = await patch({ linked_episode_id: episodeId });
    if (ok) {
      setView('main');
      onClose();
    }
  }

  async function handleExclude(): Promise<void> {
    const ok = await patch({ included_as_context: false });
    if (ok) onClose();
  }

  async function handleReinclude(): Promise<void> {
    const ok = await patch({ included_as_context: true });
    if (ok) onClose();
  }

  async function handleReincludeSeries(): Promise<void> {
    const ok = await postIncludeSeries();
    if (ok) onClose();
  }

  function close(): void {
    setView('main');
    setAction('idle');
    onClose();
  }

  // Pickers list non-archived items
  const activeTags = tags.filter((tg) => tg.archived_at === null);
  const activeEpisodes = episodes
    .filter((ep) => ep.archived_at === null)
    .sort((a, b) => (b.start_date < a.start_date ? -1 : b.start_date > a.start_date ? 1 : 0));

  return (
    <BottomSheet open={open} onClose={close} ariaLabel={t.sheetAriaLabel}>
      {view === 'main' && (
        <div className="flex flex-col gap-4 p-5">
          <div className="flex items-start justify-between gap-3">
            <div className="flex flex-col gap-1">
              <h2 className="text-lg font-semibold text-fg">{event.title}</h2>
              <p className="text-sm text-fg-muted">{dateTimeLabel}</p>
              {event.location && (
                <p className="text-sm text-fg-muted">{event.location}</p>
              )}
              {isRecurring && (
                <p className="text-xs uppercase tracking-wide text-fg-subtle">
                  {t.recurringBadge}
                </p>
              )}
            </div>
            <button
              ref={closeRef}
              type="button"
              onClick={close}
              aria-label={t.close}
              className="rounded-md p-2 text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
            >
              ✕
            </button>
          </div>

          <div className="flex flex-col gap-2">
            <button
              type="button"
              onClick={() => setView('pickingTag')}
              disabled={action === 'submitting'}
              className="inline-flex min-h-11 items-center justify-between rounded-md border border-border bg-surface px-4 py-2 text-base text-fg hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
            >
              <span>
                {linkedTag ? t.linkedTagLabel(linkedTag.label) : t.linkTagButton}
              </span>
              <span aria-hidden="true">›</span>
            </button>
            <button
              type="button"
              onClick={() => setView('pickingEpisode')}
              disabled={action === 'submitting'}
              className="inline-flex min-h-11 items-center justify-between rounded-md border border-border bg-surface px-4 py-2 text-base text-fg hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
            >
              <span>
                {linkedEpisode
                  ? t.linkedEpisodeLabel(linkedEpisode.label)
                  : t.linkEpisodeButton}
              </span>
              <span aria-hidden="true">›</span>
            </button>
          </div>

          {action === 'error' && (
            <p role="alert" className="text-sm text-fg">
              {t.actionError}
            </p>
          )}

          <div className="flex flex-col gap-2">
            {isExcluded ? (
              <>
                <button
                  type="button"
                  onClick={() => void handleReinclude()}
                  disabled={action === 'submitting'}
                  className="inline-flex min-h-11 items-center justify-center rounded-md border border-border bg-surface px-4 py-2 text-base text-fg hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
                >
                  {t.reincludeButton}
                </button>
                {isRecurring && (
                  <button
                    type="button"
                    onClick={() => void handleReincludeSeries()}
                    disabled={action === 'submitting'}
                    className="inline-flex min-h-11 items-center justify-center rounded-md border border-border bg-surface px-4 py-2 text-base text-fg hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
                  >
                    {t.reincludeSeriesButton}
                  </button>
                )}
              </>
            ) : (
              <button
                type="button"
                onClick={() => void handleExclude()}
                disabled={action === 'submitting'}
                className="inline-flex min-h-11 items-center justify-center rounded-md border border-border bg-surface px-4 py-2 text-base text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
              >
                {isRecurring ? t.excludeRecurringButton : t.excludeButton}
              </button>
            )}
          </div>
        </div>
      )}

      {view === 'pickingTag' && (
        <div className="flex flex-col gap-3 p-5">
          <div className="flex items-center justify-between gap-3">
            <button
              type="button"
              onClick={() => setView('main')}
              className="inline-flex items-center gap-1 text-base text-fg-muted hover:text-fg focus-visible:outline-2 focus-visible:outline-accent"
            >
              <span aria-hidden="true">‹</span>
              <span>{t.pickerBack}</span>
            </button>
            <h2 className="text-lg font-semibold text-fg">{t.tagPickerTitle}</h2>
            <span className="w-12" />
          </div>

          <ul className="flex flex-col gap-1">
            <li>
              <button
                type="button"
                onClick={() => void handlePickTag(null)}
                disabled={action === 'submitting'}
                className="inline-flex min-h-11 w-full items-center rounded-md border border-border bg-surface px-4 py-2 text-base text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
              >
                {t.pickerNone}
              </button>
            </li>
            {activeTags.length === 0 ? (
              <li className="text-base text-fg-muted">{t.pickerEmptyTags}</li>
            ) : (
              activeTags.map((tg) => (
                <li key={tg.id}>
                  <button
                    type="button"
                    onClick={() => void handlePickTag(tg.id)}
                    disabled={action === 'submitting'}
                    className="inline-flex min-h-11 w-full items-center rounded-md border border-border bg-surface px-4 py-2 text-base text-fg hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
                  >
                    {tg.label}
                  </button>
                </li>
              ))
            )}
          </ul>

          {action === 'error' && (
            <p role="alert" className="text-sm text-fg">
              {t.actionError}
            </p>
          )}
        </div>
      )}

      {view === 'pickingEpisode' && (
        <div className="flex flex-col gap-3 p-5">
          <div className="flex items-center justify-between gap-3">
            <button
              type="button"
              onClick={() => setView('main')}
              className="inline-flex items-center gap-1 text-base text-fg-muted hover:text-fg focus-visible:outline-2 focus-visible:outline-accent"
            >
              <span aria-hidden="true">‹</span>
              <span>{t.pickerBack}</span>
            </button>
            <h2 className="text-lg font-semibold text-fg">{t.episodePickerTitle}</h2>
            <span className="w-12" />
          </div>

          <ul className="flex flex-col gap-1">
            <li>
              <button
                type="button"
                onClick={() => void handlePickEpisode(null)}
                disabled={action === 'submitting'}
                className="inline-flex min-h-11 w-full items-center rounded-md border border-border bg-surface px-4 py-2 text-base text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
              >
                {t.pickerNone}
              </button>
            </li>
            {activeEpisodes.length === 0 ? (
              <li className="text-base text-fg-muted">{t.pickerEmptyEpisodes}</li>
            ) : (
              activeEpisodes.map((ep) => (
                <li key={ep.id}>
                  <button
                    type="button"
                    onClick={() => void handlePickEpisode(ep.id)}
                    disabled={action === 'submitting'}
                    className="inline-flex min-h-11 w-full items-center rounded-md border border-border bg-surface px-4 py-2 text-base text-fg hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
                  >
                    {ep.label}
                  </button>
                </li>
              ))
            )}
          </ul>

          {action === 'error' && (
            <p role="alert" className="text-sm text-fg">
              {t.actionError}
            </p>
          )}
        </div>
      )}
    </BottomSheet>
  );
}
