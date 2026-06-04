'use client';

// ContextEventsSection — v1.6 Phase 1.E.4.
//
// Renders the per-day Activiteiten list on the Context tab. Above
// Periodes. Sorted by start_at ascending, all-day events first.
//
// `Toon overgeslagen events` toggle reveals included_as_context=false
// rows with reduced opacity + `(overgeslagen)` suffix. Mirror of the
// `Toon gearchiveerd` toggle from v1.5b tag-management.
//
// Tap an event row → opens CalendarEventSheet. The sheet handles all
// per-event mutations (tag/episode linking + sluit-uit + voeg-hele-
// serie-toe). On close, parent re-renders via router.refresh().

import { useMemo, useState } from 'react';
import { CalendarEventSheet } from '@/components/calendar-event-sheet';
import { copy } from '@/copy';
import type { DirectusCalendarEventRow } from '@/lib/api/calendars';
import type { Episode } from '@/lib/domain/episode';
import { formatDutchTime } from '@/lib/domain/event-display';
import type { Tag } from '@/lib/domain/tag';
import { cn } from '@/lib/ui/cn';

type Props = {
  /**
   * Events overlapping the selected date. Caller pre-filters; component
   * does the sort + include/exclude visibility logic.
   */
  events: DirectusCalendarEventRow[];
  /** Tags corpus for the per-event sheet picker. */
  tags: Tag[];
  /** Episodes corpus for the per-event sheet picker. */
  episodes: Episode[];
};

function sortEvents(
  events: DirectusCalendarEventRow[],
): DirectusCalendarEventRow[] {
  return [...events].sort((a, b) => {
    // All-day first.
    if (a.all_day !== b.all_day) return a.all_day ? -1 : 1;
    // Then by start_at ascending.
    if (a.start_at < b.start_at) return -1;
    if (a.start_at > b.start_at) return 1;
    return 0;
  });
}

export function ContextEventsSection({ events, tags, episodes }: Props) {
  const t = copy.settings.calendars.contextSection;
  const [showExcluded, setShowExcluded] = useState(false);
  const [sheetEvent, setSheetEvent] = useState<DirectusCalendarEventRow | null>(null);

  const tagById = useMemo(() => {
    const m = new Map<string, Tag>();
    for (const tg of tags) m.set(tg.id, tg);
    return m;
  }, [tags]);
  const episodeById = useMemo(() => {
    const m = new Map<string, Episode>();
    for (const ep of episodes) m.set(ep.id, ep);
    return m;
  }, [episodes]);

  const visible = useMemo(() => {
    const filtered = events.filter((e) => showExcluded || e.included_as_context);
    return sortEvents(filtered);
  }, [events, showExcluded]);

  // If there are no included events AND the toggle is off, don't render
  // the section at all (empty space, no copy needed per the design).
  const anyIncluded = events.some((e) => e.included_as_context);
  const anyExcluded = events.some((e) => !e.included_as_context);
  if (!anyIncluded && !anyExcluded) return null;

  return (
    <section aria-label={t.heading} className="flex flex-col gap-3">
      <div className="flex items-baseline justify-between gap-3">
        <h2 className="text-lg font-medium text-fg">{t.heading}</h2>
        {anyExcluded && (
          <label className="flex items-center gap-2 text-sm text-fg-muted">
            <input
              type="checkbox"
              checked={showExcluded}
              onChange={(e) => setShowExcluded(e.target.checked)}
              className="h-4 w-4 accent-accent"
            />
            <span>{t.showExcluded}</span>
          </label>
        )}
      </div>

      {visible.length === 0 ? null : (
        <ul className="flex flex-col gap-2">
          {visible.map((evt) => {
            const isExcluded = !evt.included_as_context;
            const startAt = new Date(evt.start_at);
            const timeLabel = evt.all_day ? t.allDayLabel : formatDutchTime(startAt);
            const linkedTag = evt.linked_tag_id ? tagById.get(evt.linked_tag_id) : null;
            const linkedEpisode = evt.linked_episode_id
              ? episodeById.get(evt.linked_episode_id)
              : null;
            const isRecurring = evt.recurrence_id !== null;
            return (
              <li key={evt.id}>
                <button
                  type="button"
                  onClick={() => setSheetEvent(evt)}
                  className={cn(
                    'flex w-full items-baseline justify-between gap-3 rounded-md border border-border bg-surface p-3 text-left hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent',
                    isExcluded && 'opacity-50',
                  )}
                >
                  <div className="flex flex-col gap-1">
                    <div className="flex items-baseline gap-2">
                      <span className="text-sm tabular-nums text-fg-muted">{timeLabel}</span>
                      <span className="text-base text-fg">{evt.title}</span>
                      {isRecurring && (
                        <span aria-hidden="true" className="text-fg-subtle" title="Herhalend">
                          ↻
                        </span>
                      )}
                      {isExcluded && (
                        <span className="text-xs text-fg-subtle">{t.excludedSuffix}</span>
                      )}
                    </div>
                    {(linkedTag || linkedEpisode) && (
                      <div className="flex items-baseline gap-3 text-xs text-fg-muted">
                        {linkedTag && <span>→ {linkedTag.label}</span>}
                        {linkedEpisode && <span>↳ {linkedEpisode.label}</span>}
                      </div>
                    )}
                  </div>
                </button>
              </li>
            );
          })}
        </ul>
      )}

      {sheetEvent && (
        <CalendarEventSheet
          event={sheetEvent}
          tags={tags}
          episodes={episodes}
          open={true}
          onClose={() => setSheetEvent(null)}
        />
      )}
    </section>
  );
}
