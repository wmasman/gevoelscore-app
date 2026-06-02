// Pure layout helper for the timeline episode-overlay. Derives the
// linked-tag dots that render ON the episode bands at their day_entry's
// x position. Composes with computeEpisodeBandLayout so the rowIndex
// matches — same input → identical band layout → identical dot rows.

import type { DayEntry } from './day-entry';
import { computeEpisodeBandLayout } from './episode-band-layout';
import type { Episode } from './episode';
import type { Tag } from './tag';

export type LinkedTagDot = {
  date: string;
  episodeId: string;
  tagId: string;
  rowIndex: number;
};

export function computeLinkedTagDots(
  entries: DayEntry[],
  tags: Tag[],
  episodes: Episode[],
  from: string,
  to: string,
): LinkedTagDot[] {
  // Index tags + visible bands for O(1) lookups inside the entry loop.
  const tagById = new Map<string, Tag>(tags.map((t) => [t.id, t]));
  const bands = computeEpisodeBandLayout(episodes, from, to);
  const rowByEpisodeId = new Map<string, number>(
    bands.map((b) => [b.episode.id, b.rowIndex]),
  );

  const result: LinkedTagDot[] = [];
  for (const e of entries) {
    if (e.date < from || e.date > to) continue;
    for (const tagId of e.tag_ids) {
      const tag = tagById.get(tagId);
      if (!tag || tag.parent_episode_id === null) continue;
      const rowIndex = rowByEpisodeId.get(tag.parent_episode_id);
      if (rowIndex === undefined) continue;
      result.push({
        date: e.date,
        episodeId: tag.parent_episode_id,
        tagId: tag.id,
        rowIndex,
      });
    }
  }
  return result;
}
