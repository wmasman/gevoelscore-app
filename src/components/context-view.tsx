'use client';

// ContextView — the third top-level surface (Context tab). Holds context
// signals that affect the daily score over time. Today it renders a
// single Periodes section (interventies + levensgebeurtenissen); the
// container is named "Context" because v1.6 (Google Calendar bindings)
// and v2 (project context, recurring patterns) add sibling sections
// here.
//
// Tab order in the bottom nav (set by TodayShell): Context / Vandaag /
// Tijdlijn. Vandaag in the centre — best thumb-reach for the daily
// action.
//
// Step-3 scope: read-only. List items inside Periodes sub-groups are
// plain text — NOT buttons. Step-4 turns them into tappable detail
// launchers and adds the "+ Nieuwe" buttons.
//
// Data flow: episodes are server-rendered in page.tsx and threaded
// through TodayShell as a prop. No internal fetch, no client state
// shadow. Mutations (step-4) call router.refresh(); the server
// re-runs and a fresh prop arrives.
//
// Heading hierarchy:
//   h2 = "Periodes" (the section within Context)
//   h3 = "Interventies (actief)", etc. (sub-groups within Periodes)
// When v1.6 adds Calendar bindings the structure extends to another
// h2 sibling next to Periodes.

import { copy } from '@/copy';
import { formatDateDutch } from '@/lib/domain/date';
import type { Episode } from '@/lib/domain/episode';
import { groupEpisodes } from '@/lib/domain/episode-groups';

type Props = {
  episodes: Episode[];
  today: string;
};

export function ContextView({ episodes, today }: Props) {
  return (
    <section
      aria-label={copy.context.ariaLabel}
      className="flex flex-col gap-8"
    >
      <PeriodesSection episodes={episodes} today={today} />
      {/* v1.6: <CalendarBindingsSection /> goes here */}
      {/* v2:   <ProjectsSection /> + <PatronenSection /> follow */}
    </section>
  );
}

function PeriodesSection({ episodes, today }: Props) {
  const groups = groupEpisodes(episodes, today);
  const isEmpty = groups.totalActive === 0 && groups.totalDone === 0;

  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-base font-semibold text-fg">
        {copy.context.periodes.heading}
      </h2>
      {isEmpty ? (
        <p className="text-base text-fg-muted">{copy.context.periodes.empty}</p>
      ) : (
        <div className="flex flex-col gap-6">
          {groups.interventiesActive.length > 0 && (
            <Group
              title={copy.context.periodes.section.interventiesActive}
              items={groups.interventiesActive}
            />
          )}
          {groups.interventiesDone.length > 0 && (
            <Group
              title={copy.context.periodes.section.interventiesDone}
              items={groups.interventiesDone}
            />
          )}
          {groups.levensgebeurtenissenActive.length > 0 && (
            <Group
              title={copy.context.periodes.section.levensgebeurtenissenActive}
              items={groups.levensgebeurtenissenActive}
            />
          )}
          {groups.levensgebeurtenissenDone.length > 0 && (
            <Group
              title={copy.context.periodes.section.levensgebeurtenissenDone}
              items={groups.levensgebeurtenissenDone}
            />
          )}
        </div>
      )}
    </div>
  );
}

function Group({ title, items }: { title: string; items: Episode[] }) {
  return (
    <div className="flex flex-col gap-2">
      <h3 className="text-sm font-medium uppercase tracking-wider text-fg-muted">
        {title}
      </h3>
      <ul className="flex flex-col divide-y divide-border rounded-md border border-border bg-surface">
        {items.map((ep) => (
          <li key={ep.id} className="flex min-h-11 flex-col gap-1 p-4">
            <span className="text-base text-fg">{ep.label}</span>
            <span className="text-sm text-fg-subtle">
              {copy.context.periodes.dateRange(
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
