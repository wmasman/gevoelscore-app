'use client';

// ScoreChart — pure SVG line chart for the timeline view. The 1-10 score
// scale is small and the range is at most 90 days, so vanilla SVG is
// enough — no chart library (see step-6 plan for the trade-off).
//
// Visual contract per design brief:
// - Single line through logged points; missing days render as a gap, not
//   interpolated. Honest data.
// - y-axis 1..10, x-axis dates spanning [from, to] inclusive.
// - Tap a point → onPointTap(date). Tappable hit area is generous (one
//   <button> per point, positioned over the circle with absolute coords
//   inside a foreignObject? No — pointer events on the <circle> itself
//   suffice for both keyboard and mouse).
//
// Accessibility: each point is an interactive <button> rendered inside the
// SVG via a <g role="button"> with aria-label. The whole SVG carries
// role="img" + aria-label for screen readers that can't navigate the
// individual points.

import type { DayEntry } from '@/lib/domain/day-entry';

type Props = {
  entries: DayEntry[];
  from: string; // YYYY-MM-DD, inclusive
  to: string; // YYYY-MM-DD, inclusive
  onPointTap: (date: string) => void;
};

// Layout constants. The SVG fills its parent's width via viewBox; the
// height stays fixed so the chart doesn't grow vertically with phone
// size variations.
const SVG_WIDTH = 600;
const SVG_HEIGHT = 200;
const PADDING_LEFT = 28;
const PADDING_RIGHT = 12;
const PADDING_TOP = 12;
const PADDING_BOTTOM = 24;

function shiftDate(date: string, days: number): string {
  const parsed = new Date(`${date}T12:00:00Z`);
  parsed.setUTCDate(parsed.getUTCDate() + days);
  const y = parsed.getUTCFullYear();
  const m = String(parsed.getUTCMonth() + 1).padStart(2, '0');
  const d = String(parsed.getUTCDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function daysBetween(from: string, to: string): number {
  // Anchored on UTC noon to dodge DST.
  const a = new Date(`${from}T12:00:00Z`).getTime();
  const b = new Date(`${to}T12:00:00Z`).getTime();
  return Math.round((b - a) / (24 * 60 * 60 * 1000));
}

export function ScoreChart({ entries, from, to, onPointTap }: Props) {
  const totalDays = daysBetween(from, to) + 1;
  const chartW = SVG_WIDTH - PADDING_LEFT - PADDING_RIGHT;
  const chartH = SVG_HEIGHT - PADDING_TOP - PADDING_BOTTOM;
  const stepX = totalDays > 1 ? chartW / (totalDays - 1) : chartW;

  function xFor(date: string): number {
    const idx = daysBetween(from, date);
    return PADDING_LEFT + idx * stepX;
  }
  function yFor(score: number): number {
    // 1 at the bottom, 10 at the top
    return PADDING_TOP + ((10 - score) / 9) * chartH;
  }

  // Build gap-bounded segments. Two adjacent entries belong to the same
  // segment if their dates are exactly one day apart.
  const sorted = [...entries].sort((a, b) => (a.date < b.date ? -1 : 1));
  const segments: DayEntry[][] = [];
  let current: DayEntry[] = [];
  for (const e of sorted) {
    if (current.length === 0) {
      current.push(e);
      continue;
    }
    const last = current[current.length - 1]!;
    if (shiftDate(last.date, 1) === e.date) {
      current.push(e);
    } else {
      segments.push(current);
      current = [e];
    }
  }
  if (current.length > 0) segments.push(current);

  const yTicks = [1, 4, 7, 10];

  return (
    <svg
      role="img"
      aria-label="Score-tijdlijn"
      viewBox={`0 0 ${SVG_WIDTH} ${SVG_HEIGHT}`}
      preserveAspectRatio="xMidYMid meet"
      className="h-48 w-full"
    >
      {/* y-axis tick lines + labels */}
      {yTicks.map((t) => (
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
            className="fill-fg-muted text-[10px]"
          >
            {t}
          </text>
        </g>
      ))}

      {/* one path per gap-bounded segment */}
      {segments.map((seg, i) => {
        if (seg.length < 2) {
          // Single point with no line — still render the circle below.
          return null;
        }
        const d = seg
          .map((e, j) => {
            const cmd = j === 0 ? 'M' : 'L';
            return `${cmd}${xFor(e.date).toFixed(1)},${yFor(e.score).toFixed(1)}`;
          })
          .join(' ');
        return (
          <path
            key={`seg-${i}`}
            data-segment={i}
            d={d}
            fill="none"
            className="stroke-accent"
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        );
      })}

      {/* one tappable point per logged day */}
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
          {/* Larger transparent hit target so brainfog taps don't miss. */}
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
            r={4}
            className="fill-accent"
          />
        </g>
      ))}
    </svg>
  );
}
