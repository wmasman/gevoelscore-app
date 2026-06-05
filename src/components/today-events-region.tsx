'use client';

// TodayEventsRegion — step-2 Phase 2.D.
//
// Renders today's calendar events on the Today card, between Tags and
// OngoingEpisodes. Mirrors ContextEventsSection in shape but stripped
// to essentials: no excluded-toggle (today-card stays brief), no
// linked-episode line (linked-tag badge only per AC2.26), and a
// collapse-when->3 affordance to keep the card scannable when a day
// is busy.
//
// Caller pre-filters events to those overlapping today's date; this
// component drops included_as_context=false rows, sorts (all-day
// first, then start_at ascending), and renders. Empty → null (AC2.28),
// no copy needed — saves space on the Today card.
//
// Tap a row → CalendarEventSheet (re-used from step-1; no fork per
// AC2.29). All mutations live in the sheet; this component is
// presentational + state for expand/sheet-target only.

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
   * Events overlapping today (caller pre-filters by date overlap). This
   * component filters to included_as_context=true, sorts, and renders.
   */
  events: DirectusCalendarEventRow[];
  /** Tag corpus for the badge + the per-event sheet picker. */
  tags: Tag[];
  /** Episode corpus for the per-event sheet picker. */
  episodes: Episode[];
};

const COLLAPSED_VISIBLE = 3;

function sortEvents(
  events: DirectusCalendarEventRow[],
): DirectusCalendarEventRow[] {
  return [...events].sort((a, b) => {
    if (a.all_day !== b.all_day) return a.all_day ? -1 : 1;
    if (a.start_at < b.start_at) return -1;
    if (a.start_at > b.start_at) return 1;
    return 0;
  });
}

export function TodayEventsRegion({ events, tags, episodes }: Props) {
  const t = copy.home.todayEvents;
  const [expanded, setExpanded] = useState(false);
  const [sheetEvent, setSheetEvent] =
    useState<DirectusCalendarEventRow | null>(null);

  const tagById = useMemo(() => {
    const m = new Map<string, Tag>();
    for (const tg of tags) m.set(tg.id, tg);
    return m;
  }, [tags]);

  const visible = useMemo(() => {
    const included = events.filter((e) => e.included_as_context);
    return sortEvents(included);
  }, [events]);

  if (visible.length === 0) return null;

  const overflowed = visible.length > COLLAPSED_VISIBLE;
  const rows = !overflowed || expanded ? visible : visible.slice(0, COLLAPSED_VISIBLE);
  const hidden = visible.length - COLLAPSED_VISIBLE;

  return (
    <div className="flex w-full flex-col gap-2 p-4">
      <span className="text-sm text-fg-muted">{t.regionLabel}</span>
      <ul className="flex flex-col divide-y divide-border">
        {rows.map((evt) => {
          const timeLabel = evt.all_day
            ? t.allDayLabel
            : formatDutchTime(new Date(evt.start_at));
          const linkedTag = evt.linked_tag_id
            ? tagById.get(evt.linked_tag_id) ?? null
            : null;
          return (
            <li key={evt.id} className="flex">
              <button
                type="button"
                onClick={() => setSheetEvent(evt)}
                className={cn(
                  'flex min-h-11 flex-1 items-baseline gap-3 py-2 text-left',
                  'hover:bg-surface-muted focus-visible:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent',
                )}
              >
                <span className="text-sm tabular-nums text-fg-muted">
                  {timeLabel}
                </span>
                <span className="flex-1 text-base text-fg">{evt.title}</span>
                {linkedTag && (
                  <span className="rounded-full bg-accent-soft px-2 py-0.5 text-xs text-accent-active">
                    {linkedTag.label}
                  </span>
                )}
              </button>
            </li>
          );
        })}
      </ul>
      {overflowed && !expanded && (
        <button
          type="button"
          onClick={() => setExpanded(true)}
          className="inline-flex min-h-11 items-center self-start rounded-md px-3 py-2 text-sm text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
        >
          {t.expandMore(hidden)}
        </button>
      )}
      {overflowed && expanded && (
        <button
          type="button"
          onClick={() => setExpanded(false)}
          className="inline-flex min-h-11 items-center self-start rounded-md px-3 py-2 text-sm text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
        >
          {t.collapseLess}
        </button>
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
    </div>
  );
}
