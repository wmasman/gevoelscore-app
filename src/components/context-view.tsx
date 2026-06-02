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
// Step-3 scope: read-only list. Step-4 (THIS file's current state):
// launchers + tap-to-edit. Each list item is now a button that opens
// EpisodeFormSheet in edit mode; the two "+ Nieuwe" launchers open it
// in create mode with the category locked. The sheet state lives in
// THIS component, not in TodayShell — local to the surface that uses it.
//
// Data flow: episodes are server-rendered in page.tsx and threaded
// through TodayShell as a prop. Mutations call router.refresh() inside
// the hook; the server re-runs and a fresh prop arrives. No client
// state shadow.
//
// Heading hierarchy:
//   h2 = "Periodes" (the section within Context)
//   h3 = "Interventies (actief)", etc. (sub-groups within Periodes)
// When v1.6 adds Calendar bindings the structure extends to another
// h2 sibling next to Periodes.

import { useState } from 'react';
import { EpisodeFormSheet } from '@/components/episode-form-sheet';
import { copy } from '@/copy';
import { formatDateDutch } from '@/lib/domain/date';
import type { Episode } from '@/lib/domain/episode';
import type { EpisodeCategory } from '@/lib/domain/episode-category';
import { groupEpisodes } from '@/lib/domain/episode-groups';
import type { Tag } from '@/lib/domain/tag';

type Props = {
  episodes: Episode[];
  today: string;
  /** Step-5: full tag corpus, threaded into EpisodeFormSheet for the
   *  LinkedTagsSection + TagPickerSheet integration. */
  tags?: Tag[];
};

type SheetState =
  | { open: false }
  | {
      open: true;
      mode: 'create';
      category: EpisodeCategory;
      initialEpisode: null;
    }
  | {
      open: true;
      mode: 'edit';
      category: EpisodeCategory;
      initialEpisode: Episode;
    };

export function ContextView({ episodes, today, tags = [] }: Props) {
  const [sheet, setSheet] = useState<SheetState>({ open: false });

  function openCreate(category: EpisodeCategory): void {
    setSheet({ open: true, mode: 'create', category, initialEpisode: null });
  }
  function openEdit(ep: Episode): void {
    setSheet({
      open: true,
      mode: 'edit',
      category: ep.category,
      initialEpisode: ep,
    });
  }
  function closeSheet(): void {
    setSheet({ open: false });
  }

  return (
    <section
      aria-label={copy.context.ariaLabel}
      className="flex flex-col gap-8"
    >
      <PeriodesSection
        episodes={episodes}
        today={today}
        onLaunchCreate={openCreate}
        onTapEpisode={openEdit}
      />
      {/* v1.6: <CalendarBindingsSection /> goes here */}
      {/* v2:   <ProjectsSection /> + <PatronenSection /> follow */}

      {/* Sheet state lifted into ContextView so the close/refresh cycle
          coordinates with the Periodes list. Both onSaved and onArchived
          just close the sheet — the hook already triggered router.refresh,
          so the new state arrives via the episodes prop on the next render. */}
      <EpisodeFormSheet
        mode={sheet.open ? sheet.mode : 'create'}
        category={sheet.open ? sheet.category : 'interventie'}
        initialEpisode={sheet.open ? sheet.initialEpisode : null}
        today={today}
        open={sheet.open}
        onClose={closeSheet}
        onSaved={closeSheet}
        onArchived={closeSheet}
        tags={tags}
        episodes={episodes}
      />
    </section>
  );
}

type PeriodesSectionProps = {
  episodes: Episode[];
  today: string;
  onLaunchCreate: (category: EpisodeCategory) => void;
  onTapEpisode: (ep: Episode) => void;
};

function PeriodesSection({
  episodes,
  today,
  onLaunchCreate,
  onTapEpisode,
}: PeriodesSectionProps) {
  const groups = groupEpisodes(episodes, today);
  const isEmpty = groups.totalActive === 0 && groups.totalDone === 0;

  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-base font-semibold text-fg">
        {copy.context.periodes.heading}
      </h2>

      {/* Launchers — always visible (above the empty-state line OR above
          the first sub-group). Stacked on narrow screens, side-by-side
          implicit from the wrap behaviour. */}
      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          onClick={() => onLaunchCreate('interventie')}
          className="inline-flex min-h-11 items-center rounded-md border border-border bg-surface px-4 py-2 text-base text-fg hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
        >
          {copy.context.newInterventieButton}
        </button>
        <button
          type="button"
          onClick={() => onLaunchCreate('levensgebeurtenis')}
          className="inline-flex min-h-11 items-center rounded-md border border-border bg-surface px-4 py-2 text-base text-fg hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
        >
          {copy.context.newPeriodeButton}
        </button>
      </div>

      {isEmpty ? (
        <p className="text-base text-fg-muted">{copy.context.periodes.empty}</p>
      ) : (
        <div className="flex flex-col gap-6">
          {groups.interventiesActive.length > 0 && (
            <Group
              title={copy.context.periodes.section.interventiesActive}
              items={groups.interventiesActive}
              onTap={onTapEpisode}
            />
          )}
          {groups.interventiesDone.length > 0 && (
            <Group
              title={copy.context.periodes.section.interventiesDone}
              items={groups.interventiesDone}
              onTap={onTapEpisode}
            />
          )}
          {groups.levensgebeurtenissenActive.length > 0 && (
            <Group
              title={copy.context.periodes.section.levensgebeurtenissenActive}
              items={groups.levensgebeurtenissenActive}
              onTap={onTapEpisode}
            />
          )}
          {groups.levensgebeurtenissenDone.length > 0 && (
            <Group
              title={copy.context.periodes.section.levensgebeurtenissenDone}
              items={groups.levensgebeurtenissenDone}
              onTap={onTapEpisode}
            />
          )}
        </div>
      )}
    </div>
  );
}

function Group({
  title,
  items,
  onTap,
}: {
  title: string;
  items: Episode[];
  onTap: (ep: Episode) => void;
}) {
  return (
    <div className="flex flex-col gap-2">
      <h3 className="text-sm font-medium uppercase tracking-wider text-fg-muted">
        {title}
      </h3>
      <ul className="flex flex-col divide-y divide-border rounded-md border border-border bg-surface">
        {items.map((ep) => {
          const startNl = formatDateDutch(ep.start_date);
          const endNl = ep.end_date === null ? null : formatDateDutch(ep.end_date);
          return (
            <li key={ep.id} className="flex">
              <button
                type="button"
                onClick={() => onTap(ep)}
                aria-label={copy.context.form.listItemAriaLabel(ep.label, startNl, endNl)}
                className="flex min-h-11 flex-1 flex-col gap-1 p-4 text-left hover:bg-surface-muted focus-visible:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
              >
                <span className="text-base text-fg">{ep.label}</span>
                <span className="text-sm text-fg-subtle">
                  {copy.context.periodes.dateRange(startNl, endNl)}
                </span>
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
