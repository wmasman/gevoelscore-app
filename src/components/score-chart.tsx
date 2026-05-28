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

import type { DayEntry } from '@/lib/domain/day-entry';
import { movingAverage } from '@/lib/domain/moving-average';

type Props = {
  entries: DayEntry[];
  from: string; // YYYY-MM-DD, inclusive
  to: string; // YYYY-MM-DD, inclusive
  onPointTap: (date: string) => void;
};

const SVG_WIDTH = 600;
const SVG_HEIGHT = 200;
const PADDING_LEFT = 28;
const PADDING_RIGHT = 12;
const PADDING_TOP = 12;
const PADDING_BOTTOM = 24;

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

export function ScoreChart({ entries, from, to, onPointTap }: Props) {
  const totalDays = daysBetween(from, to) + 1;
  const chartW = SVG_WIDTH - PADDING_LEFT - PADDING_RIGHT;
  const chartH = SVG_HEIGHT - PADDING_TOP - PADDING_BOTTOM;
  const stepX = totalDays > 1 ? chartW / (totalDays - 1) : chartW;

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
