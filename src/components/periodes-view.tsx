'use client';

// PeriodesView — Blok 3 of the v1.5 verloop-and-episodes feature. The
// third top-level surface (between Vandaag and Tijdlijn) that renders
// the user's Episodes as a read-only list grouped by category × active
// vs afgerond.
//
// Step-3 scope: read-only display. List items are plain text — NOT
// buttons. Step-4 turns them into tappable detail-launchers and adds
// the "+ Nieuwe interventie" / "+ Nieuwe periode" buttons.
//
// Data flow: episodes are server-rendered in page.tsx and threaded
// down through TodayShell as a prop. No internal fetch, no client
// state shadow. After mutations land in step-4, router.refresh()
// re-runs the server component and a fresh prop arrives.
//
// Grouping logic lives in src/lib/domain/episode-groups.ts — pure,
// fully unit-tested without React.

import { copy } from '@/copy';
import { formatDateDutch } from '@/lib/domain/date';
import type { Episode } from '@/lib/domain/episode';
import { groupEpisodes } from '@/lib/domain/episode-groups';

type Props = {
  episodes: Episode[];
  today: string;
};

export function PeriodesView({ episodes, today }: Props) {
  const groups = groupEpisodes(episodes, today);

  // Treat all-archived (or genuinely empty) as the empty state — the
  // user sees the same message either way.
  if (groups.totalActive === 0 && groups.totalDone === 0) {
    return (
      <section
        aria-label={copy.periodes.ariaLabel}
        className="flex flex-col gap-4"
      >
        <p className="text-base text-fg-muted">{copy.periodes.empty}</p>
      </section>
    );
  }

  return (
    <section
      aria-label={copy.periodes.ariaLabel}
      className="flex flex-col gap-6"
    >
      {groups.interventiesActive.length > 0 && (
        <Group
          title={copy.periodes.section.interventiesActive}
          items={groups.interventiesActive}
        />
      )}
      {groups.interventiesDone.length > 0 && (
        <Group
          title={copy.periodes.section.interventiesDone}
          items={groups.interventiesDone}
        />
      )}
      {groups.levensgebeurtenissenActive.length > 0 && (
        <Group
          title={copy.periodes.section.levensgebeurtenissenActive}
          items={groups.levensgebeurtenissenActive}
        />
      )}
      {groups.levensgebeurtenissenDone.length > 0 && (
        <Group
          title={copy.periodes.section.levensgebeurtenissenDone}
          items={groups.levensgebeurtenissenDone}
        />
      )}
    </section>
  );
}

function Group({ title, items }: { title: string; items: Episode[] }) {
  return (
    <div className="flex flex-col gap-2">
      <h2 className="text-sm font-medium uppercase tracking-wider text-fg-muted">
        {title}
      </h2>
      <ul className="flex flex-col divide-y divide-border rounded-md border border-border bg-surface">
        {items.map((ep) => (
          <li key={ep.id} className="flex min-h-11 flex-col gap-1 p-4">
            <span className="text-base text-fg">{ep.label}</span>
            <span className="text-sm text-fg-subtle">
              {copy.periodes.dateRange(
                formatDateDutch(ep.start_date),
                ep.end_date === null ? null : formatDateDutch(ep.end_date),
              )}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
