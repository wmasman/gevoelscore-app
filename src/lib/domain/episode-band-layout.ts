// Pure layout helper for the timeline episode-overlay feature. Translates
// a list of episodes + a visible date range into a deterministic set of
// bands grouped into rows (greedy stacking). The chart component is thin:
// it derives the layout via this helper and renders rectangles at the
// returned positions.
//
// Date arithmetic uses string comparison — YYYY-MM-DD ISO dates compare
// correctly with `<`, `<=`, `>`, `>=` lexicographically, so no Date math
// is needed for overlap checks. End_date null means "lopend" (ongoing);
// clamped to `to` (the right edge of the visible range).

import type { Episode } from './episode';

export type EpisodeBand = {
  episode: Episode;
  rowIndex: number;
  xStartDate: string;
  xEndDate: string;
};

function clamp(date: string, lo: string, hi: string): string {
  if (date < lo) return lo;
  if (date > hi) return hi;
  return date;
}

export function computeEpisodeBandLayout(
  episodes: Episode[],
  from: string,
  to: string,
): EpisodeBand[] {
  // Filter: archived OR no overlap with [from, to] → out.
  const visible = episodes.filter((e) => {
    if (e.archived_at !== null) return false;
    const effectiveEnd = e.end_date ?? '9999-12-31';
    // Overlap check: [start, end] vs [from, to] overlap iff start <= to AND end >= from.
    return e.start_date <= to && effectiveEnd >= from;
  });

  // Sort by start_date asc, ties broken by id lex. Deterministic.
  visible.sort((a, b) => {
    if (a.start_date !== b.start_date) {
      return a.start_date < b.start_date ? -1 : 1;
    }
    return a.id < b.id ? -1 : a.id > b.id ? 1 : 0;
  });

  // Greedy row assignment. `rowEnds[i]` = the xEndDate of the last band
  // placed in row i. A new band fits in row i iff its xStartDate > rowEnds[i].
  const rowEnds: string[] = [];
  const result: EpisodeBand[] = [];

  for (const e of visible) {
    const xStartDate = clamp(e.start_date, from, to);
    const xEndDate = clamp(e.end_date ?? to, from, to);

    let rowIndex = -1;
    for (let i = 0; i < rowEnds.length; i += 1) {
      if (xStartDate > rowEnds[i]!) {
        rowIndex = i;
        break;
      }
    }
    if (rowIndex === -1) {
      rowIndex = rowEnds.length;
      rowEnds.push(xEndDate);
    } else {
      rowEnds[rowIndex] = xEndDate;
    }

    result.push({ episode: e, rowIndex, xStartDate, xEndDate });
  }

  return result;
}
