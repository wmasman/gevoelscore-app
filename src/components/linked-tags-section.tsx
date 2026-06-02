'use client';

// LinkedTagsSection — the step-5 affordance that lives inside the edit-mode
// EpisodeFormSheet. Pure presentational: filters the global tags list to
// the ones linked to THIS episode, renders chips with one-tap unlink, and
// hosts the "+ Tag" button that opens the picker. The picker itself is
// owned by EpisodeFormSheet; this component only signals the open intent.

import { copy } from '@/copy';
import type { Episode } from '@/lib/domain/episode';
import type { Tag } from '@/lib/domain/tag';

type Props = {
  episode: Episode;
  tags: Tag[];
  onUnlink: (tagId: string) => void;
  onOpenPicker: () => void;
  disabled: boolean;
};

export function LinkedTagsSection({
  episode,
  tags,
  onUnlink,
  onOpenPicker,
  disabled,
}: Props) {
  const linked = tags.filter((t) => t.parent_episode_id === episode.id);

  return (
    <div className="flex flex-col gap-2">
      <h3 className="text-sm font-medium uppercase tracking-wider text-fg-muted">
        {copy.context.tagLinking.heading}
      </h3>
      {linked.length === 0 ? (
        <p className="text-sm text-fg-muted">{copy.context.tagLinking.empty}</p>
      ) : (
        <ul className="flex flex-wrap gap-2">
          {linked.map((t) => (
            <li
              key={t.id}
              className="inline-flex items-center gap-1 rounded-full border border-border bg-surface px-3 py-1 text-sm text-fg"
            >
              <span>{t.label}</span>
              <button
                type="button"
                onClick={() => onUnlink(t.id)}
                disabled={disabled}
                aria-label={copy.context.tagLinking.unlinkAriaLabel(t.label)}
                className="inline-flex h-7 min-w-7 items-center justify-center rounded-full text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:cursor-not-allowed disabled:opacity-60"
              >
                ✕
              </button>
            </li>
          ))}
        </ul>
      )}
      <div>
        <button
          type="button"
          onClick={onOpenPicker}
          disabled={disabled}
          className="inline-flex min-h-11 items-center rounded-md border border-border bg-surface px-4 py-2 text-base text-fg hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:cursor-not-allowed disabled:opacity-60"
        >
          {copy.context.tagLinking.addButton}
        </button>
      </div>
    </div>
  );
}
