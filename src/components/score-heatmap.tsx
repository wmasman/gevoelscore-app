'use client';

// ScoreHeatmap — experimental alternative to the line chart. Each day in
// the [from, to] range is a coloured cell; logged days take a five-band
// accent intensity (low score → pale, high → vibrant), missing days
// render as outlined empty cells. Tapping any cell opens the day-detail
// sheet — same callback contract as ScoreChart's onPointTap.
//
// Why a heatmap: the line chart answers "how am I trending?", but a
// calendar grid answers "where did the bad weeks cluster?" — different
// pattern-recognition. Brainfog-friendly because the eye can compare
// adjacent cells without re-reading axis values.
//
// Layout: 7-column ISO-week grid (Monday-first, Dutch convention). Rows
// run oldest week at top → most-recent week at bottom. Cells outside the
// [from, to] range render as transparent placeholders so the rectangular
// grid stays intact.
//
// Touch target: each cell is a 44×44 button (WCAG 2.5.5, brainfog floor).

import type { DayEntry } from '@/lib/domain/day-entry';
import type { Episode } from '@/lib/domain/episode';
import type { EpisodeCategory } from '@/lib/domain/episode-category';

type Props = {
  entries: DayEntry[];
  from: string;
  to: string;
  onCellTap: (date: string) => void;
  /**
   * Episode-overlay (2026-06-02). When provided, each in-range day-cell
   * that falls within a non-archived (and non-filtered) episode's range
   * gets a 3px left-edge stripe per overlapping episode, stacked
   * horizontally. The cell's score-intensity tint stays primary; the
   * stripes are the secondary signal.
   */
  episodes?: Episode[];
  categoriesVisible?: Record<EpisodeCategory, boolean>;
};

const WEEKDAY_LABELS = ['Ma', 'Di', 'Wo', 'Do', 'Vr', 'Za', 'Zo'] as const;

function shiftDate(date: string, days: number): string {
  const parsed = new Date(`${date}T12:00:00Z`);
  parsed.setUTCDate(parsed.getUTCDate() + days);
  const y = parsed.getUTCFullYear();
  const m = String(parsed.getUTCMonth() + 1).padStart(2, '0');
  const d = String(parsed.getUTCDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

// ISO weekday: Monday = 0, ..., Sunday = 6.
function isoWeekday(date: string): number {
  const parsed = new Date(`${date}T12:00:00Z`);
  const jsDay = parsed.getUTCDay(); // Sun = 0
  return (jsDay + 6) % 7;
}

// Five-band intensity. Discrete bands beat continuous gradients here
// because the eye distinguishes ~5 levels reliably and brainfog adds
// noise to fine discrimination.
function bandPct(score: number): number {
  if (score <= 2) return 22;
  if (score <= 4) return 40;
  if (score <= 6) return 58;
  if (score <= 8) return 76;
  return 100;
}

function cellBackground(score: number | undefined): string {
  if (score === undefined) return 'transparent';
  const pct = bandPct(score);
  // color-mix gives a clean visual blend without needing a sprite of
  // pre-mixed palette stops.
  return `color-mix(in srgb, var(--color-accent) ${pct}%, var(--color-bg))`;
}

function dayNumber(date: string): string {
  return date.slice(8, 10).replace(/^0/, '');
}

export function ScoreHeatmap({
  entries,
  from,
  to,
  onCellTap,
  episodes = [],
  categoriesVisible,
}: Props) {
  const byDate = new Map<string, number>();
  for (const e of entries) byDate.set(e.date, e.score);

  // Pre-filter episodes once. Archived + category-filtered + out-of-range
  // are dropped before the per-cell overlap loop. Sort by start_date asc
  // (then id) so stripes stack deterministically left-to-right.
  const visibleEpisodes = episodes
    .filter((ep) => {
      if (ep.archived_at !== null) return false;
      if (categoriesVisible && categoriesVisible[ep.category] === false) {
        return false;
      }
      const effectiveEnd = ep.end_date ?? '9999-12-31';
      return ep.start_date <= to && effectiveEnd >= from;
    })
    .sort((a, b) => {
      if (a.start_date !== b.start_date) {
        return a.start_date < b.start_date ? -1 : 1;
      }
      return a.id < b.id ? -1 : a.id > b.id ? 1 : 0;
    });

  function episodesOnDate(date: string): Episode[] {
    return visibleEpisodes.filter((ep) => {
      const end = ep.end_date ?? '9999-12-31';
      return ep.start_date <= date && end >= date;
    });
  }

  // Find the Monday of `from`'s week and the Sunday of `to`'s week so
  // the grid is rectangular.
  const gridStart = shiftDate(from, -isoWeekday(from));
  const gridEnd = shiftDate(to, 6 - isoWeekday(to));

  // Build rows of 7 cells.
  const rows: string[][] = [];
  let cursor = gridStart;
  while (cursor <= gridEnd) {
    const row: string[] = [];
    for (let i = 0; i < 7; i += 1) {
      row.push(cursor);
      cursor = shiftDate(cursor, 1);
    }
    rows.push(row);
  }

  return (
    <div
      role="grid"
      aria-label="Score-heatmap"
      className="flex flex-col gap-1"
    >
      <div role="row" className="grid grid-cols-7 gap-1 px-0">
        {WEEKDAY_LABELS.map((label) => (
          <div
            key={label}
            role="columnheader"
            className="text-center text-xs font-medium text-fg-muted"
          >
            {label}
          </div>
        ))}
      </div>
      {rows.map((row) => (
        <div key={row[0]} role="row" className="grid grid-cols-7 gap-1">
          {row.map((date) => {
            const inRange = date >= from && date <= to;
            const score = inRange ? byDate.get(date) : undefined;
            if (!inRange) {
              return (
                <div
                  key={date}
                  role="gridcell"
                  aria-hidden="true"
                  className="aspect-square"
                />
              );
            }
            const logged = score !== undefined;
            const label = logged
              ? `${date}: score ${score}`
              : `${date}: geen score`;
            const bg = cellBackground(score);
            const overlapping = episodesOnDate(date);
            return (
              <div
                key={date}
                role="gridcell"
                className="relative aspect-square"
              >
                <button
                  type="button"
                  aria-label={label}
                  data-date={date}
                  data-score={score ?? ''}
                  onClick={() => onCellTap(date)}
                  style={{ backgroundColor: bg }}
                  className={
                    'h-full w-full min-h-11 rounded-md text-xs font-medium text-fg ' +
                    'focus-visible:outline-2 focus-visible:outline-accent ' +
                    (logged
                      ? 'border border-transparent'
                      : 'border border-border bg-surface-muted/40 text-fg-subtle')
                  }
                >
                  {dayNumber(date)}
                </button>
                {overlapping.length > 0 && (
                  <div
                    aria-hidden="true"
                    className="pointer-events-none absolute inset-y-0 left-0 flex"
                  >
                    {overlapping.map((ep) => (
                      <div
                        key={ep.id}
                        data-episode-stripe={ep.id}
                        data-episode-category={ep.category}
                        className={
                          'w-0.75 ' +
                          (ep.category === 'interventie'
                            ? 'bg-accent'
                            : 'bg-fg-subtle')
                        }
                        style={{
                          opacity:
                            ep.category === 'interventie' ? 0.6 : 0.5,
                        }}
                      />
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}
