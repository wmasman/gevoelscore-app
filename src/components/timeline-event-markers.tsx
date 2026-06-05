'use client';

// TimelineEventMarkers — step-3 Phase 3.B.
//
// SVG overlay rendered on top of the existing ScoreChart container.
// Two visual primitives:
//   - faint horizontal bars for multi-day spans, layered behind the
//     score line so the line stays the dominant element (AC3.10)
//   - thin warm-earth ticks at the top edge of the chart for each day
//     that has an included-as-context event (AC3.8, AC3.9)
//
// Spans render first, ticks second -> SVG paint order draws ticks ON
// TOP of spans, matching AC3.19's z-order requirement.
//
// Tap targets are enlarged 44x44 invisible rects (AC3.13) so the
// brainfog-friendly touch target survives even when the visible tick
// is only a few pixels wide. The pointer goes to the SAME date for
// ticks (the date itself) and spans (the span's start date).
//
// Pure presentational. Layout state comes from buildEventOverlayLayout
// (Phase 3.A) via the parent; this component does not derive overlap
// or filtering of its own (AC3.14).
//
// x-coordinate mapping: each day is a slot of width = width / numDays.
// Slot CENTERS land at slotWidth/2, slotWidth*1.5, etc. The visual
// tick sits at the slot center; spans run from the start-slot center
// to the end-slot center.

import { copy } from '@/copy';

type Props = {
  /** Days that have at least one included-as-context event. */
  markerDays: Set<string>;
  /** Events crossing >= 1 local-midnight boundary (rendered as a bar). */
  spans: Array<{
    recurrenceId: string | null;
    startDate: string;
    endDate: string;
  }>;
  /** Leftmost x = fromDate's slot. yyyy-mm-dd, inclusive. */
  fromDate: string;
  /** Rightmost x = toDate's slot. yyyy-mm-dd, inclusive. */
  toDate: string;
  /** Pixel width of the chart area. */
  width: number;
  /** Pixel height of the chart area (drives the span height). */
  height: number;
  /** Tap handler. Receives the tapped date (ticks) or the span's start (spans). */
  onDateSelect: (date: string) => void;
};

const TICK_STRIP_HEIGHT = 8;
const TICK_VISIBLE_WIDTH = 2;
const TICK_VISIBLE_HEIGHT = 6;
const TAP_ZONE_SIZE = 44;
const SPAN_FILL = 'var(--color-fg-subtle)';
const SPAN_OPACITY = 0.15;
const TICK_FILL = 'var(--color-fg-subtle)';

function daysBetween(from: string, to: string): number {
  const fy = Number(from.slice(0, 4));
  const fm = Number(from.slice(5, 7));
  const fd = Number(from.slice(8, 10));
  const ty = Number(to.slice(0, 4));
  const tm = Number(to.slice(5, 7));
  const td = Number(to.slice(8, 10));
  const fromUtc = Date.UTC(fy, fm - 1, fd);
  const toUtc = Date.UTC(ty, tm - 1, td);
  return Math.round((toUtc - fromUtc) / 86400000) + 1;
}

function dayIndex(date: string, from: string): number {
  return daysBetween(from, date) - 1;
}

export function TimelineEventMarkers({
  markerDays,
  spans,
  fromDate,
  toDate,
  width,
  height,
  onDateSelect,
}: Props) {
  if (markerDays.size === 0 && spans.length === 0) return null;

  const t = copy.timeline.eventMarkers;
  const numDays = daysBetween(fromDate, toDate);
  const slotWidth = width / numDays;
  const centerOf = (date: string): number =>
    dayIndex(date, fromDate) * slotWidth + slotWidth / 2;

  const totalSvgHeight = TICK_STRIP_HEIGHT + height;
  // Span bar height = a fraction of the chart so the line still dominates.
  const spanY = TICK_STRIP_HEIGHT + height * 0.3;
  const spanH = height * 0.4;

  return (
    <svg
      width={width}
      height={totalSvgHeight}
      role="presentation"
      style={{ overflow: 'visible' }}
    >
      {/* Spans first so ticks paint on top (AC3.19). */}
      {spans.map((span) => {
        const x1 = centerOf(span.startDate);
        const x2 = centerOf(span.endDate);
        const w = Math.max(x2 - x1, 1);
        // Tap zone is the wider of the visible bar or the 44px minimum,
        // centered on the bar.
        const tapW = Math.max(w, TAP_ZONE_SIZE);
        const tapX = x1 + w / 2 - tapW / 2;
        const tapY = TICK_STRIP_HEIGHT + height / 2 - TAP_ZONE_SIZE / 2;
        return (
          <g
            key={`span-${span.startDate}-${span.endDate}-${span.recurrenceId ?? 'one-off'}`}
            data-kind="span"
          >
            <rect
              data-visual-mark="span"
              x={x1}
              y={spanY}
              width={w}
              height={spanH}
              fill={SPAN_FILL}
              opacity={SPAN_OPACITY}
              pointerEvents="none"
            />
            <rect
              x={tapX}
              y={tapY}
              width={tapW}
              height={TAP_ZONE_SIZE}
              fill="transparent"
              role="button"
              aria-label={t.spanAriaLabel(span.startDate, span.endDate)}
              onClick={() => onDateSelect(span.startDate)}
              style={{ cursor: 'pointer' }}
            />
          </g>
        );
      })}

      {/* Ticks last so they sit on top. */}
      {[...markerDays].map((date) => {
        const cx = centerOf(date);
        const tapX = cx - TAP_ZONE_SIZE / 2;
        return (
          <g key={`tick-${date}`} data-kind="tick">
            <rect
              data-visual-mark="tick"
              x={cx - TICK_VISIBLE_WIDTH / 2}
              y={1}
              width={TICK_VISIBLE_WIDTH}
              height={TICK_VISIBLE_HEIGHT}
              fill={TICK_FILL}
              pointerEvents="none"
            />
            <rect
              x={tapX}
              y={0}
              width={TAP_ZONE_SIZE}
              height={TAP_ZONE_SIZE}
              fill="transparent"
              role="button"
              aria-label={t.tickAriaLabel(date)}
              onClick={() => onDateSelect(date)}
              style={{ cursor: 'pointer' }}
            />
          </g>
        );
      })}
    </svg>
  );
}
