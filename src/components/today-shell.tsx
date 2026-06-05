'use client';

// TodayShell — the home screen after Step 4 of quick-entry-popout.
//
// Structure on the Today tab:
//   - Today card: 3 tappable regions (score / note / tags) that summarise
//     today's saved values. Tapping any region opens the QuickEntryFlow
//     popout at the matching step.
//   - "Vorige dagen" list: 3 most-recent past-day cards by default,
//     "Toon meer" expands inline up to 10. Each past-day card tap opens
//     the popout for that date with isPastDay=true.
//   - QuickEntryFlow: state-driven open/close. Auto-opens at the score
//     step on first render when today has no entry yet.
//
// End-of-flow signal: when QuickEntryFlow fires onComplete we close the
// sheet and pulse the target card (today-card or the relevant past-day
// card) for 200ms via a data-attribute that drives a Tailwind colour
// transition. No checkmark, no text — the pulse is the entire signal,
// per the design brief's "motion as communication" rule.
//
// SaveStatusProvider stays for the Tijdlijn tab's nested DayDetailSheet
// (it has its own provider scope but the parent provider is harmless).
// The page-header glyph from Step 4b was removed: the popout's end-of-
// flow pulse is now the success signal; the banner below handles errors.

import { useEffect, useMemo, useRef, useState } from 'react';
import { usePrefersReducedMotion } from '@/hooks/use-prefers-reduced-motion';
import Link from 'next/link';
import { ContextView } from '@/components/context-view';
import { EpisodeFormSheet } from '@/components/episode-form-sheet';
import { QuickEntryFlow } from '@/components/lab/quick-entry-flow';
import { SaveAnnouncer } from '@/components/save-announcer';
import { SaveStatus } from '@/components/save-status';
import {
  SaveStatusProvider,
  useMergedSaveStatus,
} from '@/components/save-status-context';
import { TimelineView } from '@/components/timeline-view';
import { TodayEventsRegion } from '@/components/today-events-region';
import { copy } from '@/copy';
import type { DirectusCalendarEventRow } from '@/lib/api/calendars';
import type { DayEntry } from '@/lib/domain/day-entry';
import { formatDateDutch } from '@/lib/domain/date';
import type { Episode } from '@/lib/domain/episode';
import type { Tag } from '@/lib/domain/tag';
import { computeRecencyByTagId } from '@/lib/domain/tag-sort';
import { cn } from '@/lib/ui/cn';

type Props = {
  date: string;
  entry: DayEntry | null;
  allTags: Tag[];
  timelineEntries: DayEntry[];
  /**
   * Episodes for the v1.5 Context tab (Periodes section). Server-
   * rendered through page.tsx via readAllEpisodes (active-only).
   * Optional default-empty keeps existing component tests passing —
   * only the Context tab branch reads the prop.
   */
  episodes?: Episode[];
  /**
   * v1.6 Phase 1.E.4: calendar events overlapping `date`, rendered in
   * the Context tab's Activiteiten section. Optional default-empty
   * keeps existing tests + first-paint safety.
   */
  calendarEvents?: DirectusCalendarEventRow[];
  /**
   * Step-3 Phase 3.C: events overlapping the 30-day timeline range,
   * forwarded into TimelineView for the TimelineEventMarkers SVG
   * overlay. Distinct from `calendarEvents` (today-only) so the
   * Context tab + Today card don't have to learn date-filtering.
   */
  timelineCalendarEvents?: DirectusCalendarEventRow[];
};

type Tab = 'context' | 'today' | 'timeline';
type Step = 'score' | 'note' | 'tags';

const DEFAULT_VISIBLE_PAST_DAYS = 3;
const MAX_VISIBLE_PAST_DAYS = 10;
const PULSE_DURATION_MS = 200;

export function TodayShell({
  date,
  entry,
  allTags,
  timelineEntries,
  episodes = [],
  calendarEvents = [],
  timelineCalendarEvents = [],
}: Props) {
  return (
    <SaveStatusProvider>
      <TodayShellInner
        date={date}
        entry={entry}
        allTags={allTags}
        timelineEntries={timelineEntries}
        episodes={episodes}
        calendarEvents={calendarEvents}
        timelineCalendarEvents={timelineCalendarEvents}
      />
    </SaveStatusProvider>
  );
}

function TodayShellInner({
  date,
  entry,
  allTags,
  timelineEntries,
  episodes = [],
  calendarEvents = [],
  timelineCalendarEvents = [],
}: Props) {
  const [tab, setTab] = useState<Tab>('today');
  const merged = useMergedSaveStatus();
  // Today-card ongoing-episodes region: tapping a row opens the in-place
  // EpisodeFormSheet for that episode. State lives at the shell level so
  // the form is mounted once even though the row is inside TodayCard.
  const [ongoingEditTarget, setOngoingEditTarget] = useState<Episode | null>(
    null,
  );
  // When reduce-motion is set we skip the pulse entirely — the
  // SaveAnnouncer's "Opgeslagen." live-region announcement carries the
  // completion signal for those users (A-M5).
  const prefersReducedMotion = usePrefersReducedMotion();

  // `entry` is read straight from the server-rendered prop. After any
  // save useDayEntryUpsert calls router.refresh(); the server component
  // re-runs, a fresh `entry` flows in, and the today-card display
  // updates without any client-side state shadow. The earlier
  // useState(entry) mirror + explicit GET refetch was load-bearing for
  // a single use case (display refresh after save) but introduced two
  // sources of truth; the router.refresh path is one.

  // Sheet state. `target` carries the date + entry being edited.
  type SheetState = {
    open: boolean;
    date: string;
    entry: DayEntry | null;
    startStep: Step;
    isPastDay: boolean;
  };
  const [sheet, setSheet] = useState<SheetState>(() => ({
    open: entry === null,
    date,
    entry,
    startStep: 'score',
    isPastDay: false,
  }));

  // Which card to pulse next — the today-card or a specific past-day's
  // date string. Cleared after PULSE_DURATION_MS.
  const [pulseKey, setPulseKey] = useState<string | null>(null);
  const pulseTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  useEffect(() => {
    return () => {
      if (pulseTimerRef.current !== null) clearTimeout(pulseTimerRef.current);
    };
  }, []);

  function openSheetFor(target: { date: string; entry: DayEntry | null; isPastDay: boolean }, startStep: Step): void {
    setSheet({
      open: true,
      date: target.date,
      entry: target.entry,
      startStep,
      isPastDay: target.isPastDay,
    });
  }

  function handleClose(): void {
    setSheet((s) => ({ ...s, open: false }));
  }

  function handleComplete(): void {
    const key = sheet.isPastDay ? sheet.date : 'today';
    setSheet((s) => ({ ...s, open: false }));
    if (prefersReducedMotion) return;
    setPulseKey(key);
    if (pulseTimerRef.current !== null) clearTimeout(pulseTimerRef.current);
    pulseTimerRef.current = setTimeout(() => {
      setPulseKey(null);
    }, PULSE_DURATION_MS);
  }

  // Tag-picker recency map: derive once from the 30-day timeline window.
  // Drives the within-category recency sort in TagCategoryList (v1.5a).
  // Same map flows to both the today-card popout and (via TimelineView)
  // the past-day-edit popout.
  const recencyByTagId = useMemo(
    () => computeRecencyByTagId(timelineEntries),
    [timelineEntries],
  );

  // Past-day list. Exclude today, sort by date descending, cap at 10.
  const [expanded, setExpanded] = useState(false);
  const pastEntries = timelineEntries
    .filter((e) => e.date < date)
    .slice()
    .sort((a, b) => (a.date > b.date ? -1 : 1))
    .slice(0, MAX_VISIBLE_PAST_DAYS);
  const visiblePast = expanded ? pastEntries : pastEntries.slice(0, DEFAULT_VISIBLE_PAST_DAYS);

  return (
    <>
      <main className="mx-auto flex min-h-dvh max-w-120 flex-col gap-6 p-6 pb-[calc(5rem+env(safe-area-inset-bottom))]">
        <header className="flex flex-row items-baseline justify-between gap-3">
        <h1 className="text-2xl font-semibold capitalize">
          {formatDateDutch(date)}
        </h1>
        <Link
          href="/settings"
          aria-label={copy.settings.iconLabel}
          className="inline-flex min-h-11 min-w-11 items-center justify-center rounded-md text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
        >
          <svg
            aria-hidden="true"
            viewBox="0 0 24 24"
            width="20"
            height="20"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <circle cx="12" cy="12" r="3" />
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06A2 2 0 1 1 4.27 16.94l.06-.06A1.65 1.65 0 0 0 4.66 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06A2 2 0 1 1 7.04 4.29l.06.06A1.65 1.65 0 0 0 8.92 4.66a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
          </svg>
        </Link>
      </header>

      {tab === 'context' ? (
        <ContextView
          episodes={episodes}
          today={date}
          tags={allTags}
          calendarEvents={calendarEvents}
        />
      ) : tab === 'today' ? (
        <div className="flex flex-col gap-6">
          <TodayCard
            entry={entry}
            allTags={allTags}
            pulsing={pulseKey === 'today'}
            onTapRegion={(step) =>
              openSheetFor({ date, entry, isPastDay: false }, step)
            }
            todayEvents={calendarEvents}
            episodes={episodes}
            ongoingEpisodes={episodes.filter(
              (e) =>
                e.archived_at === null &&
                (e.end_date === null || e.end_date >= date),
            )}
            onEpisodeTap={(ep) => setOngoingEditTarget(ep)}
          />

          {pastEntries.length > 0 && (
            <section aria-labelledby="vorige-dagen" className="flex flex-col gap-3">
              <h2 id="vorige-dagen" className="text-base font-medium text-fg-muted">
                {copy.home.previousHeading}
              </h2>
              <ul className="flex flex-col gap-2">
                {visiblePast.map((e) => (
                  <li key={e.date}>
                    <PastDayCard
                      entry={e}
                      pulsing={pulseKey === e.date}
                      onTap={() =>
                        openSheetFor({ date: e.date, entry: e, isPastDay: true }, 'score')
                      }
                    />
                  </li>
                ))}
              </ul>
              {pastEntries.length > DEFAULT_VISIBLE_PAST_DAYS && (
                <button
                  type="button"
                  onClick={() => setExpanded((v) => !v)}
                  className="inline-flex min-h-11 items-center self-start rounded-md px-3 py-2 text-sm text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
                >
                  {expanded ? copy.home.showLess : copy.home.showMore}
                </button>
              )}
            </section>
          )}

          <QuickEntryFlow
            date={sheet.date}
            initialEntry={sheet.entry}
            allTags={allTags}
            recencyByTagId={recencyByTagId}
            open={sheet.open}
            startStep={sheet.startStep}
            isPastDay={sheet.isPastDay}
            // In edit mode dismissal IS completion — the user came in
            // to change one field, did so, and tapped away. Pulse the
            // card so they get the same end-of-interaction signal as
            // the fresh-entry "Klaar" path.
            onClose={sheet.entry !== null ? handleComplete : handleClose}
            onComplete={handleComplete}
          />

          {/* In-place EpisodeFormSheet for the ongoing-episodes region
              at the bottom of the today-card. Same sheet as Context tab
              + Tijdlijn band-tap; centralised so saving from any
              surface goes through the same hook + router.refresh. */}
          <EpisodeFormSheet
            mode="edit"
            category={ongoingEditTarget?.category ?? 'interventie'}
            initialEpisode={ongoingEditTarget}
            today={date}
            open={ongoingEditTarget !== null}
            onClose={() => setOngoingEditTarget(null)}
            onSaved={() => setOngoingEditTarget(null)}
            onArchived={() => setOngoingEditTarget(null)}
            tags={allTags}
            episodes={episodes}
          />
        </div>
      ) : (
        <TimelineView
          today={date}
          initialEntries={timelineEntries}
          allTags={allTags}
          recencyByTagId={recencyByTagId}
          episodes={episodes}
          calendarEvents={timelineCalendarEvents}
        />
      )}

      {merged.status === 'error' && tab === 'today' && (
        <SaveStatus status="error" error={merged.error} variant="banner" />
      )}

      {/* Single page-level live region. Announces "Opgeslagen." after
          every save completion (throttled), "Niet opgeslagen..." on
          errors. Hidden visually; the pulse + the banner above carry
          the sighted-user feedback. See save-announcer.tsx + A-H4 in
          the 2026-05-30 audit. */}
        <SaveAnnouncer />
      </main>

      {/* Bottom tab bar — M-H2 from the 2026-05-30 audit. Tabs at the
          top of the screen broke the project's own thumb-first rule
          and Apple HIG (primary nav lives at the bottom for one-handed
          reach). Fixed-position outside of <main>; main has bottom
          padding to account for it. z-30 sits under the BottomSheet
          (z-40/50) so the popout overlays the bar when open. */}
      <nav
        aria-label={copy.home.tabsAriaLabel}
        className="fixed bottom-0 left-0 right-0 z-30 border-t border-border bg-surface pb-[env(safe-area-inset-bottom)]"
      >
        <div
          role="tablist"
          aria-label={copy.home.tabsAriaLabel}
          className="mx-auto flex max-w-120 px-2"
        >
          {/* Tab order: Context / Vandaag / Tijdlijn. Vandaag sits in the
              CENTRE so the daily-flow action is equally reachable from
              either thumb on both right-hand and left-hand grip. */}
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'context'}
            onClick={() => setTab('context')}
            className={cn(
              'flex min-h-14 flex-1 items-center justify-center px-3 py-2 text-base focus-visible:outline-2 focus-visible:outline-accent',
              tab === 'context' ? 'font-medium text-accent' : 'text-fg-muted',
            )}
          >
            {copy.context.title}
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'today'}
            onClick={() => setTab('today')}
            className={cn(
              'flex min-h-14 flex-1 items-center justify-center px-3 py-2 text-base focus-visible:outline-2 focus-visible:outline-accent',
              tab === 'today' ? 'font-medium text-accent' : 'text-fg-muted',
            )}
          >
            {copy.timeline.todayTab}
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'timeline'}
            onClick={() => setTab('timeline')}
            className={cn(
              'flex min-h-14 flex-1 items-center justify-center px-3 py-2 text-base focus-visible:outline-2 focus-visible:outline-accent',
              tab === 'timeline' ? 'font-medium text-accent' : 'text-fg-muted',
            )}
          >
            {copy.timeline.title}
          </button>
        </div>
      </nav>
    </>
  );
}

// --- Today-card ------------------------------------------------------------

type TodayCardProps = {
  entry: DayEntry | null;
  allTags: Tag[];
  pulsing: boolean;
  onTapRegion: (step: Step) => void;
  /**
   * Step-2 today-card events (2026-06-05). Events overlapping today
   * (server-pre-filtered by date overlap in page.tsx via
   * readCalendarEventsInRange). The TodayEventsRegion further filters
   * to included_as_context=true and renders nothing when empty.
   */
  todayEvents?: DirectusCalendarEventRow[];
  /**
   * Full episodes corpus for the CalendarEventSheet's episode-picker
   * surface. Independent of `ongoingEpisodes` which is the filtered
   * subset that drives the OngoingEpisodesRegion list itself.
   */
  episodes?: Episode[];
  /**
   * Step-1 today-card ongoing-episodes (2026-06-02). Pre-filtered list
   * of episodes where end_date is null AND archived_at is null. The
   * region only renders when this is non-empty.
   */
  ongoingEpisodes?: Episode[];
  onEpisodeTap?: (episode: Episode) => void;
};

// Three vertically-stacked editable regions, hairline-divided. Each
// region carries an explicit pencil icon as the edit affordance — without
// it, users (correctly) don't infer that the read-only summary is
// tappable. The icon stays visible at all times to keep the affordance
// brainfog-discoverable.

function TodayCard({
  entry,
  allTags,
  pulsing,
  onTapRegion,
  todayEvents = [],
  episodes = [],
  ongoingEpisodes = [],
  onEpisodeTap,
}: TodayCardProps) {
  return (
    <article
      data-testid="today-card"
      data-pulsing={pulsing ? 'true' : 'false'}
      className={cn(
        'flex flex-col divide-y divide-border rounded-md border border-border',
        'bg-surface transition-colors duration-200 ease-out',
        // `!` so the pulse always wins over the hover/focus background —
        // otherwise a hover during the 200ms pulse window could swap to
        // surface-muted and visually consume the completion signal.
        'data-[pulsing=true]:bg-accent-soft!',
      )}
    >
      <ScoreRegion score={entry?.score ?? null} onClick={() => onTapRegion('score')} />
      <NoteRegion note={entry?.note ?? null} onClick={() => onTapRegion('note')} />
      <TagsRegion
        tagIds={entry?.tag_ids ?? []}
        allTags={allTags}
        onClick={() => onTapRegion('tags')}
      />
      <TodayEventsRegion
        events={todayEvents}
        tags={allTags}
        episodes={episodes}
      />
      {ongoingEpisodes.length > 0 && onEpisodeTap !== undefined && (
        <OngoingEpisodesRegion
          episodes={ongoingEpisodes}
          onEpisodeTap={onEpisodeTap}
        />
      )}
    </article>
  );
}

function OngoingEpisodesRegion({
  episodes,
  onEpisodeTap,
}: {
  episodes: Episode[];
  onEpisodeTap: (episode: Episode) => void;
}) {
  return (
    <div className="flex w-full flex-col gap-2 p-4">
      <span className="text-sm text-fg-muted">
        {copy.home.ongoingRegionLabel}
      </span>
      <ul className="flex flex-col divide-y divide-border">
        {episodes.map((ep) => (
          <li key={ep.id} className="flex">
            <button
              type="button"
              onClick={() => onEpisodeTap(ep)}
              aria-label={copy.home.ongoingEditAriaLabel(ep.label)}
              className={cn(
                'flex min-h-11 flex-1 items-center justify-between gap-3 py-2 text-left',
                'hover:bg-surface-muted focus-visible:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent',
              )}
            >
              <span className="text-base text-fg">{ep.label}</span>
              <EditIcon />
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

function ScoreRegion({ score, onClick }: { score: number | null; onClick: () => void }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={`${copy.home.scoreRegionLabel}: ${score ?? copy.home.scoreEmpty}`}
      className={cn(
        'flex w-full items-start justify-between gap-3 p-4 text-left',
        'hover:bg-surface-muted focus-visible:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent',
      )}
    >
      {score !== null ? (
        <span className="flex items-baseline gap-3">
          <span className="text-5xl font-semibold leading-none text-accent">{score}</span>
          <span className="text-base text-fg-muted">{copy.home.scoreRegionLabel}</span>
        </span>
      ) : (
        <span className="flex flex-col">
          <span className="text-sm text-fg-muted">{copy.home.scoreRegionLabel}</span>
          <span className="text-base text-fg-muted">{copy.home.scoreEmpty}</span>
        </span>
      )}
      <EditIcon />
    </button>
  );
}

function NoteRegion({ note, onClick }: { note: string | null; onClick: () => void }) {
  const truncated = truncate(note, 140);
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={`${copy.home.noteRegionLabel}: ${truncated ?? copy.home.noteEmpty}`}
      className={cn(
        'flex w-full flex-col items-start gap-2 p-4 text-left',
        'hover:bg-surface-muted focus-visible:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent',
      )}
    >
      <span className="flex w-full items-baseline justify-between gap-3">
        <span className="text-sm text-fg-muted">{copy.home.noteRegionLabel}</span>
        <EditIcon />
      </span>
      <span className={cn('text-base', truncated ? 'text-fg' : 'text-fg-muted')}>
        {truncated ?? copy.home.noteEmpty}
      </span>
    </button>
  );
}

function TagsRegion({
  tagIds,
  allTags,
  onClick,
}: {
  tagIds: string[];
  allTags: Tag[];
  onClick: () => void;
}) {
  const tags = tagIds
    .map((id) => allTags.find((t) => t.id === id))
    .filter((t): t is Tag => t !== undefined);
  const ariaValue =
    tags.length > 0 ? tags.map((t) => t.label).join(', ') : copy.home.tagsEmpty;
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={`${copy.home.tagsRegionLabel}: ${ariaValue}`}
      className={cn(
        'flex w-full flex-col items-start gap-2 p-4 text-left',
        'hover:bg-surface-muted focus-visible:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent',
      )}
    >
      <span className="flex w-full items-baseline justify-between gap-3">
        <span className="text-sm text-fg-muted">{copy.home.tagsRegionLabel}</span>
        <EditIcon />
      </span>
      {tags.length > 0 ? (
        <span className="flex flex-wrap gap-1.5">
          {tags.map((tag) => (
            <span
              key={tag.id}
              className="rounded-full bg-accent-soft px-3 py-0.5 text-sm text-accent-active"
            >
              {tag.label}
            </span>
          ))}
        </span>
      ) : (
        <span className="text-base text-fg-muted">{copy.home.tagsEmpty}</span>
      )}
    </button>
  );
}

function EditIcon() {
  return (
    <svg
      aria-label={copy.home.editAriaLabel}
      role="img"
      viewBox="0 0 24 24"
      width="16"
      height="16"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="shrink-0 text-fg-subtle"
    >
      <path d="M12 20h9" />
      <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z" />
    </svg>
  );
}

// --- Past-day card ---------------------------------------------------------

type PastDayCardProps = {
  entry: DayEntry;
  pulsing: boolean;
  onTap: () => void;
};

function PastDayCard({ entry, pulsing, onTap }: PastDayCardProps) {
  const preview = truncate(entry.note, 50);
  return (
    <button
      type="button"
      onClick={onTap}
      data-pulsing={pulsing ? 'true' : 'false'}
      aria-label={copy.home.pastDayAriaLabel(formatDateDutch(entry.date), entry.score)}
      className={cn(
        'flex w-full items-baseline justify-between gap-3 rounded-md border border-border p-3 text-left',
        'bg-surface transition-colors duration-200 ease-out',
        'hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent',
        // `!` so the pulse always wins over the hover/focus background —
        // otherwise a hover during the 200ms pulse window could swap to
        // surface-muted and visually consume the completion signal.
        'data-[pulsing=true]:bg-accent-soft!',
      )}
    >
      <span className="flex flex-col">
        <span className="text-xs uppercase tracking-wide text-fg-muted">
          {formatDateDutch(entry.date)}
        </span>
        {preview !== null && (
          <span className="text-sm text-fg-muted">{preview}</span>
        )}
      </span>
      <span className="text-lg font-semibold text-fg">{entry.score}</span>
    </button>
  );
}

function truncate(value: string | null | undefined, max: number): string | null {
  if (!value) return null;
  if (value.length <= max) return value;
  return value.slice(0, max - 1) + '…';
}
