'use client';

// ScoreChart — pure SVG line chart for the timeline view. The 1-10 score
// scale is small and the range is at most 90 days, so vanilla SVG is
// enough — no chart library.
//
// Central visual: a smooth 7-day trailing moving average (the
// "is-this-week-better-than-last-week" line). Raw daily points are still
// rendered (smaller, muted) and remain tappable, so the user can drill
// into a single day, but they are no longer the line.
//
// Y-axis adapts to the score range present in the selected period — a
// flat run of 6's and 7's no longer gets squeezed into the bottom of a
// 1..10 chart. Falls back to 1..10 when the dataset is empty.
//
// Missing days render as gaps (in both raw segments and the MA line),
// never interpolated. Honest data — same principle as the rest of the app.
//
// Accessibility: each raw point is a keyboard-reachable button (role on
// the <g>) with an aria-label. The whole SVG carries role="img" + label.

import { formatDateDutch } from '@/lib/domain/date';
import type { DayEntry } from '@/lib/domain/day-entry';
import {
  computeEpisodeBandLayout,
  type EpisodeBand,
} from '@/lib/domain/episode-band-layout';
import type { Episode } from '@/lib/domain/episode';
import type { EpisodeCategory } from '@/lib/domain/episode-category';
import { computeLinkedTagDots } from '@/lib/domain/linked-tag-dots';
import { movingAverage } from '@/lib/domain/moving-average';
import type { Tag } from '@/lib/domain/tag';

type Props = {
  entries: DayEntry[];
  from: string; // YYYY-MM-DD, inclusive
  to: string; // YYYY-MM-DD, inclusive
  onPointTap: (date: string) => void;
  /**
   * Episode-overlay (2026-06-02). Optional with safe defaults so the
   * pre-step-1 callers + tests keep working. When provided + non-empty,
   * the chart renders bands below the score plot and dots on the bands
   * for any linked tags. Filter applies before layout.
   */
  episodes?: Episode[];
  allTags?: Tag[];
  categoriesVisible?: Record<EpisodeCategory, boolean>;
  onEpisodeTap?: (episode: Episode) => void;
};

const SVG_WIDTH = 600;
const SCORE_PLOT_HEIGHT = 200;
const PADDING_LEFT = 28;
const PADDING_RIGHT = 12;
const PADDING_TOP = 12;
const PADDING_BOTTOM = 24;

// Band-strip dimensions (step-1 episode overlay).
const BAND_ROW_HEIGHT = 8;
const BAND_GAP = 2; // visible band height = BAND_ROW_HEIGHT - BAND_GAP
const BAND_STRIP_PADDING_TOP = 6;
const BAND_STRIP_PADDING_BOTTOM = 4;

const MA_WINDOW_DAYS = 7;
// Minimum vertical span of the y-axis. A flat 7-7-7 range would compress
// the chart visually; enforce at least 3 score-points of headroom so the
// MA line has somewhere to live.
const MIN_Y_SPAN = 3;

function daysBetween(from: string, to: string): number {
  const a = new Date(`${from}T12:00:00Z`).getTime();
  const b = new Date(`${to}T12:00:00Z`).getTime();
  return Math.round((b - a) / (24 * 60 * 60 * 1000));
}

function shiftDate(date: string, days: number): string {
  const parsed = new Date(`${date}T12:00:00Z`);
  parsed.setUTCDate(parsed.getUTCDate() + days);
  const y = parsed.getUTCFullYear();
  const m = String(parsed.getUTCMonth() + 1).padStart(2, '0');
  const d = String(parsed.getUTCDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function computeYRange(entries: DayEntry[]): { lo: number; hi: number; ticks: number[] } {
  if (entries.length === 0) return { lo: 1, hi: 10, ticks: [1, 4, 7, 10] };
  let lo: number = entries[0]!.score;
  let hi: number = entries[0]!.score;
  for (const e of entries) {
    if (e.score < lo) lo = e.score;
    if (e.score > hi) hi = e.score;
  }
  // Pad outward to integers with breathing room.
  lo = Math.max(1, Math.floor(lo - 0.5));
  hi = Math.min(10, Math.ceil(hi + 0.5));
  // Enforce minimum span.
  if (hi - lo < MIN_Y_SPAN) {
    const need = MIN_Y_SPAN - (hi - lo);
    const downBy = Math.min(need, lo - 1);
    lo -= downBy;
    hi = Math.min(10, hi + (need - downBy));
  }
  // 4 evenly spaced integer ticks across [lo, hi]. Span is small (≤9), so
  // a handful of ticks reads cleanly without crowding.
  const span = hi - lo;
  const tickCount = span <= 4 ? span + 1 : 4;
  const ticks: number[] = [];
  for (let i = 0; i < tickCount; i += 1) {
    ticks.push(Math.round(lo + (span * i) / (tickCount - 1)));
  }
  return { lo, hi, ticks: Array.from(new Set(ticks)) };
}

export function ScoreChart({
  entries,
  from,
  to,
  onPointTap,
  episodes = [],
  allTags = [],
  categoriesVisible,
  onEpisodeTap,
}: Props) {
  const totalDays = daysBetween(from, to) + 1;
  const chartW = SVG_WIDTH - PADDING_LEFT - PADDING_RIGHT;
  const chartH = SCORE_PLOT_HEIGHT - PADDING_TOP - PADDING_BOTTOM;
  const stepX = totalDays > 1 ? chartW / (totalDays - 1) : chartW;

  // Apply category filter BEFORE layout. Undefined filter = all visible.
  const filteredEpisodes =
    categoriesVisible === undefined
      ? episodes
      : episodes.filter((e) => categoriesVisible[e.category] !== false);
  const bands: EpisodeBand[] = computeEpisodeBandLayout(
    filteredEpisodes,
    from,
    to,
  );
  const linkedDots = computeLinkedTagDots(
    entries,
    allTags,
    filteredEpisodes,
    from,
    to,
  );
  const rowCount =
    bands.length === 0 ? 0 : Math.max(...bands.map((b) => b.rowIndex)) + 1;
  const bandStripHeight =
    rowCount === 0
      ? 0
      : BAND_STRIP_PADDING_TOP +
        rowCount * BAND_ROW_HEIGHT +
        BAND_STRIP_PADDING_BOTTOM;
  const SVG_HEIGHT = SCORE_PLOT_HEIGHT + bandStripHeight;
  const BAND_STRIP_TOP = SCORE_PLOT_HEIGHT + BAND_STRIP_PADDING_TOP;

  function bandY(rowIndex: number): number {
    return BAND_STRIP_TOP + rowIndex * BAND_ROW_HEIGHT;
  }

  // Look up tag + episode metadata for the linked-tag dot aria-labels.
  const tagById = new Map<string, Tag>(allTags.map((t) => [t.id, t]));
  const episodeById = new Map<string, Episode>(
    episodes.map((e) => [e.id, e]),
  );

  const { lo, hi, ticks } = computeYRange(entries);
  const ySpan = hi - lo;

  function xFor(date: string): number {
    const idx = daysBetween(from, date);
    return PADDING_LEFT + idx * stepX;
  }
  function yFor(score: number): number {
    return PADDING_TOP + ((hi - score) / ySpan) * chartH;
  }

  const sorted = [...entries].sort((a, b) => (a.date < b.date ? -1 : 1));

  // Gap indicator (2026-06-02, features/timeline-gap-indicator): one
  // hollow dot per unlogged day in [from, to], placed at the chart
  // bottom (just above the x-axis). Honest data: the chart shouldn't
  // silently elide missing days; the user gets a quiet, neutral marker
  // they can tap to retroactively log. No visible "geen score" copy —
  // the aria-label carries the meaning for assistive tech.
  const loggedDates = new Set(entries.map((e) => e.date));
  const missingDates: string[] = [];
  for (let i = 0; i < totalDays; i += 1) {
    const d = shiftDate(from, i);
    if (!loggedDates.has(d)) missingDates.push(d);
  }
  const GAP_DOT_R = 3;
  const GAP_Y = PADDING_TOP + chartH - GAP_DOT_R;

  // Moving-average line: one path with M/L commands, but break into
  // sub-paths when a day yields null (window not yet warm enough OR a
  // long gap depopulated the trailing window). Same gap-honesty rule.
  const ma = movingAverage(entries, MA_WINDOW_DAYS, from, to);
  const maPathD = (() => {
    const parts: string[] = [];
    let pendingMove = true;
    for (const p of ma) {
      if (p.average === null) {
        pendingMove = true;
        continue;
      }
      const x = xFor(p.date).toFixed(1);
      const y = yFor(p.average).toFixed(1);
      parts.push(`${pendingMove ? 'M' : 'L'}${x},${y}`);
      pendingMove = false;
    }
    // A single isolated point isn't a "line" — only emit if at least one
    // line segment exists (i.e. ≥2 consecutive non-null averages).
    let lineSegments = 0;
    for (const cmd of parts) if (cmd.startsWith('L')) lineSegments += 1;
    return lineSegments === 0 ? '' : parts.join(' ');
  })();

  return (
    <svg
      role="img"
      aria-label="Score-tijdlijn met 7-daags voortschrijdend gemiddelde"
      viewBox={`0 0 ${SVG_WIDTH} ${SVG_HEIGHT}`}
      preserveAspectRatio="xMidYMid meet"
      className="h-48 w-full"
    >
      {ticks.map((t) => (
        <g key={t}>
          <line
            x1={PADDING_LEFT}
            x2={SVG_WIDTH - PADDING_RIGHT}
            y1={yFor(t)}
            y2={yFor(t)}
            className="stroke-border"
            strokeWidth={1}
          />
          <text
            x={PADDING_LEFT - 6}
            y={yFor(t) + 4}
            textAnchor="end"
            data-axis="y"
            className="fill-fg-muted text-[10px]"
          >
            {t}
          </text>
        </g>
      ))}

      {/* Moving-average line — the primary visual. */}
      <path
        data-line="ma"
        d={maPathD}
        fill="none"
        className="stroke-accent"
        strokeWidth={2.5}
        strokeLinecap="round"
        strokeLinejoin="round"
      />

      {/* Gap indicators — one hollow dot per missing day at the chart
          bottom. Rendered before raw points so logged-day dots sit on
          top in the (rare) case the bottom y collides. */}
      {missingDates.map((date) => (
        <g
          key={`gap-${date}`}
          role="button"
          tabIndex={0}
          aria-label={`${date}: geen score`}
          data-date={date}
          data-missing="true"
          onClick={() => onPointTap(date)}
          onKeyDown={(ev) => {
            if (ev.key === 'Enter' || ev.key === ' ') {
              ev.preventDefault();
              onPointTap(date);
            }
          }}
          className="cursor-pointer focus-visible:outline-2 focus-visible:outline-accent"
        >
          {/* Generous transparent hit target — matches raw-point pattern. */}
          <circle cx={xFor(date)} cy={GAP_Y} r={12} fill="transparent" />
          <circle
            cx={xFor(date)}
            cy={GAP_Y}
            r={GAP_DOT_R}
            fill="none"
            className="stroke-fg-subtle"
            strokeWidth={1}
            opacity={0.3}
          />
        </g>
      ))}

      {/* Episode bands (step-1 timeline-episode-overlay). Sit BELOW the
          score plot in their own strip. Each band is a rectangle spanning
          the episode's clamped date range; tappable to open the
          EpisodeFormSheet (handler comes from the parent). */}
      {bands.map((b) => {
        const x = xFor(b.xStartDate);
        const width = Math.max(2, xFor(b.xEndDate) - x);
        const y = bandY(b.rowIndex);
        const height = BAND_ROW_HEIGHT - BAND_GAP;
        const startDutch = formatDateDutch(b.episode.start_date);
        const endDutch =
          b.episode.end_date === null
            ? 'lopend'
            : formatDateDutch(b.episode.end_date);
        const ariaLabel = `${b.episode.label} (${startDutch} t/m ${endDutch}), tik om te bewerken`;
        return (
          <g
            key={`band-${b.episode.id}`}
            role="button"
            tabIndex={0}
            aria-label={ariaLabel}
            data-episode-id={b.episode.id}
            data-episode-category={b.episode.category}
            onClick={() => onEpisodeTap?.(b.episode)}
            onKeyDown={(ev) => {
              if (ev.key === 'Enter' || ev.key === ' ') {
                ev.preventDefault();
                onEpisodeTap?.(b.episode);
              }
            }}
            className="cursor-pointer focus-visible:outline-2 focus-visible:outline-accent"
          >
            <rect
              data-episode-id={b.episode.id}
              data-episode-category={b.episode.category}
              x={x}
              y={y}
              width={width}
              height={height}
              className={
                b.episode.category === 'interventie'
                  ? 'fill-accent'
                  : 'fill-fg-subtle'
              }
              opacity={b.episode.category === 'interventie' ? 0.3 : 0.25}
              rx={2}
            />
          </g>
        );
      })}

      {/* Linked-tag dots — render ON the band at the tag's day. Tap
          opens the QuickEntryFlow for that day (same handler as raw
          points + gap dots). */}
      {linkedDots.map((d) => {
        const tag = tagById.get(d.tagId);
        const episode = episodeById.get(d.episodeId);
        if (!tag || !episode) return null;
        const cx = xFor(d.date);
        const cy = bandY(d.rowIndex) + (BAND_ROW_HEIGHT - BAND_GAP) / 2;
        const dutchDate = formatDateDutch(d.date);
        const ariaLabel = `${dutchDate}: ${tag.label} (binnen ${episode.label})`;
        return (
          <g
            key={`linked-${d.date}-${d.tagId}`}
            role="button"
            tabIndex={0}
            aria-label={ariaLabel}
            data-date={d.date}
            onClick={() => onPointTap(d.date)}
            onKeyDown={(ev) => {
              if (ev.key === 'Enter' || ev.key === ' ') {
                ev.preventDefault();
                onPointTap(d.date);
              }
            }}
            className="cursor-pointer focus-visible:outline-2 focus-visible:outline-accent"
          >
            <circle
              data-tag-id={d.tagId}
              data-episode-id={d.episodeId}
              cx={cx}
              cy={cy}
              r={3}
              className={
                episode.category === 'interventie'
                  ? 'fill-accent'
                  : 'fill-fg-subtle'
              }
              opacity={1}
            />
          </g>
        );
      })}

      {/* Raw daily points — secondary, muted, but still tappable. */}
      {sorted.map((e) => (
        <g
          key={e.date}
          role="button"
          tabIndex={0}
          aria-label={`${e.date}: score ${e.score}`}
          data-date={e.date}
          onClick={() => onPointTap(e.date)}
          onKeyDown={(ev) => {
            if (ev.key === 'Enter' || ev.key === ' ') {
              ev.preventDefault();
              onPointTap(e.date);
            }
          }}
          className="cursor-pointer focus-visible:outline-2 focus-visible:outline-accent"
        >
          {/* Generous transparent hit target. */}
          <circle
            cx={xFor(e.date)}
            cy={yFor(e.score)}
            r={12}
            fill="transparent"
          />
          <circle
            data-date={e.date}
            cx={xFor(e.date)}
            cy={yFor(e.score)}
            r={3}
            className="fill-fg-muted"
            opacity={0.6}
          />
        </g>
      ))}
    </svg>
  );
}
