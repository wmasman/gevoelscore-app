// Pure helper that splits a list of Episodes into four display buckets
// for the Periodes tab (v1.5):
//   1. interventiesActive          — category=interventie, not yet ended
//   2. interventiesDone            — category=interventie, end_date < today
//   3. levensgebeurtenissenActive  — category=levensgebeurtenis, not yet ended
//   4. levensgebeurtenissenDone    — category=levensgebeurtenis, end_date < today
//
// Archived episodes (archived_at !== null) are excluded entirely. The
// "active episodes only" default at the API layer already filters them
// at the wire, but this client-side filter keeps the grouping correct
// even if a future caller passes archived episodes in (e.g. an admin
// debug view).
//
// "Active" means "not yet completed" — covering both ongoing (end_date
// null) AND upcoming (end_date in the future). end_date == today counts
// as active (today is inclusive — an episode ending today is still in
// progress until tomorrow).
//
// Sort: active buckets sort by start_date DESC (newest first). Done
// buckets sort by end_date DESC (most recently ended first). Both
// follow "what's relevant now" surfacing.

import type { Episode } from './episode';

export type EpisodeGroups = {
  interventiesActive: Episode[];
  interventiesDone: Episode[];
  levensgebeurtenissenActive: Episode[];
  levensgebeurtenissenDone: Episode[];
  totalActive: number;
  totalDone: number;
};

export function groupEpisodes(
  episodes: Episode[],
  today: string,
): EpisodeGroups {
  const out: EpisodeGroups = {
    interventiesActive: [],
    interventiesDone: [],
    levensgebeurtenissenActive: [],
    levensgebeurtenissenDone: [],
    totalActive: 0,
    totalDone: 0,
  };

  for (const ep of episodes) {
    if (ep.archived_at !== null) continue;
    // ISO YYYY-MM-DD strings compare lexicographically AND chronologically.
    // No timezone math here — the dates are calendar dates, not timestamps.
    const isActive = ep.end_date === null || ep.end_date >= today;
    if (ep.category === 'interventie') {
      if (isActive) out.interventiesActive.push(ep);
      else out.interventiesDone.push(ep);
    } else if (ep.category === 'levensgebeurtenis') {
      if (isActive) out.levensgebeurtenissenActive.push(ep);
      else out.levensgebeurtenissenDone.push(ep);
    }
  }

  out.interventiesActive.sort((a, b) =>
    a.start_date > b.start_date ? -1 : 1,
  );
  out.interventiesDone.sort((a, b) =>
    (a.end_date ?? '') > (b.end_date ?? '') ? -1 : 1,
  );
  out.levensgebeurtenissenActive.sort((a, b) =>
    a.start_date > b.start_date ? -1 : 1,
  );
  out.levensgebeurtenissenDone.sort((a, b) =>
    (a.end_date ?? '') > (b.end_date ?? '') ? -1 : 1,
  );

  out.totalActive =
    out.interventiesActive.length + out.levensgebeurtenissenActive.length;
  out.totalDone =
    out.interventiesDone.length + out.levensgebeurtenissenDone.length;

  return out;
}
